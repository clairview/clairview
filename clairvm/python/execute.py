from datetime import timedelta
import re
import time
from copy import deepcopy
from typing import Any, Optional, TYPE_CHECKING
from collections.abc import Callable

from clairvm.python.debugger import debugger, color_bytecode
from clairvm.python.objects import is_hog_error, new_hog_closure, CallFrame, ThrowFrame, new_hog_callable, is_hog_upvalue
from clairvm.python.operation import Operation, CLAIRQL_BYTECODE_IDENTIFIER, CLAIRQL_BYTECODE_IDENTIFIER_V0
from clairvm.python.stl import STL
from clairvm.python.stl.bytecode import BYTECODE_STL
from dataclasses import dataclass

from clairvm.python.utils import (
    UncaughtClairVMException,
    ClairVMException,
    get_nested_value,
    like,
    set_nested_value,
    calculate_cost,
    unify_comparison_types,
)

if TYPE_CHECKING:
    from clairview.models import Team

MAX_MEMORY = 64 * 1024 * 1024  # 64 MB
MAX_FUNCTION_ARGS_LENGTH = 300


@dataclass
class BytecodeResult:
    result: Any
    bytecode: list[Any]
    stdout: list[str]


def execute_bytecode(
    bytecode: list[Any],
    globals: Optional[dict[str, Any]] = None,
    functions: Optional[dict[str, Callable[..., Any]]] = None,
    timeout=timedelta(seconds=5),
    team: Optional["Team"] = None,
    debug=False,
) -> BytecodeResult:
    if len(bytecode) == 0 or (bytecode[0] != CLAIRQL_BYTECODE_IDENTIFIER and bytecode[0] != CLAIRQL_BYTECODE_IDENTIFIER_V0):
        raise ClairVMException(f"Invalid bytecode. Must start with '{CLAIRQL_BYTECODE_IDENTIFIER}'")
    version = bytecode[1] if len(bytecode) >= 2 and bytecode[0] == CLAIRQL_BYTECODE_IDENTIFIER else 0
    result = None
    start_time = time.time()
    last_op = len(bytecode) - 1
    stack: list = []
    upvalues: list[dict] = []
    upvalues_by_id: dict[int, dict] = {}
    mem_stack: list = []
    call_stack: list[CallFrame] = []
    throw_stack: list[ThrowFrame] = []
    declared_functions: dict[str, tuple[int, int]] = {}
    mem_used = 0
    max_mem_used = 0
    ops = 0
    stdout: list[str] = []
    colored_bytecode = color_bytecode(bytecode) if debug else []
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    if len(call_stack) == 0:
        call_stack.append(
            CallFrame(
                ip=2 if bytecode[0] == CLAIRQL_BYTECODE_IDENTIFIER else 1,
                chunk="root",
                stack_start=0,
                arg_len=0,
                closure=new_hog_closure(
                    new_hog_callable(
                        type="main",
                        arg_count=0,
                        upvalue_count=0,
                        ip=2 if bytecode[0] == CLAIRQL_BYTECODE_IDENTIFIER else 1,
                        chunk="root",
                        name="",
                    )
                ),
            )
        )
    frame = call_stack[-1]
    chunk_bytecode: list[Any] = bytecode

    def set_chunk_bytecode():
        nonlocal chunk_bytecode, last_op
        if not frame.chunk or frame.chunk == "root":
            chunk_bytecode = bytecode
            last_op = len(bytecode) - 1
        elif frame.chunk.startswith("stl/") and frame.chunk[4:] in BYTECODE_STL:
            chunk_bytecode = BYTECODE_STL[frame.chunk[4:]][1]
            last_op = len(bytecode) - 1
        else:
            raise ClairVMException(f"Unknown chunk: {frame.chunk}")

    def stack_keep_first_elements(count: int) -> list[Any]:
        nonlocal stack, mem_stack, mem_used
        if count < 0 or len(stack) < count:
            raise ClairVMException("Stack underflow")
        for upvalue in reversed(upvalues):
            if upvalue["location"] >= count:
                if not upvalue["closed"]:
                    upvalue["closed"] = True
                    upvalue["value"] = stack[upvalue["location"]]
            else:
                break
        removed = stack[count:]
        stack = stack[0:count]
        mem_used -= sum(mem_stack[count:])
        mem_stack = mem_stack[0:count]
        return removed

    def next_token():
        nonlocal frame, chunk_bytecode
        if frame.ip >= last_op:
            raise ClairVMException("Unexpected end of bytecode")
        frame.ip += 1
        return chunk_bytecode[frame.ip]

    def pop_stack():
        if not stack:
            raise ClairVMException("Stack underflow")
        nonlocal mem_used
        mem_used -= mem_stack.pop()
        return stack.pop()

    def push_stack(value):
        stack.append(value)
        mem_stack.append(calculate_cost(value))
        nonlocal mem_used
        mem_used += mem_stack[-1]
        nonlocal max_mem_used
        max_mem_used = max(mem_used, max_mem_used)
        if mem_used > MAX_MEMORY:
            raise ClairVMException(f"Memory limit of {MAX_MEMORY} bytes exceeded. Tried to allocate {mem_used} bytes.")

    def check_timeout():
        if time.time() - start_time > timeout.total_seconds() and not debug:
            raise ClairVMException(f"Execution timed out after {timeout.total_seconds()} seconds. Performed {ops} ops.")

    def capture_upvalue(index) -> dict:
        nonlocal upvalues
        for upvalue in reversed(upvalues):
            if upvalue["location"] < index:
                break
            if upvalue["location"] == index:
                return upvalue
        created_upvalue = {
            "__hogUpValue__": True,
            "location": index,
            "closed": False,
            "value": None,
            "id": len(upvalues) + 1,
        }
        upvalues.append(created_upvalue)
        upvalues_by_id[created_upvalue["id"]] = created_upvalue
        upvalues.sort(key=lambda x: x["location"])
        return created_upvalue

    symbol: Any = None
    while frame.ip <= last_op:
        ops += 1
        symbol = chunk_bytecode[frame.ip]
        if (ops & 127) == 0:  # every 128th operation
            check_timeout()
        elif debug:
            debugger(symbol, bytecode, colored_bytecode, frame.ip, stack, call_stack, throw_stack)
        match symbol:
            case None:
                break
            case Operation.STRING:
                push_stack(next_token())
            case Operation.INTEGER:
                push_stack(next_token())
            case Operation.FLOAT:
                push_stack(next_token())
            case Operation.TRUE:
                push_stack(True)
            case Operation.FALSE:
                push_stack(False)
            case Operation.NULL:
                push_stack(None)
            case Operation.NOT:
                push_stack(not pop_stack())
            case Operation.AND:
                push_stack(all([pop_stack() for _ in range(next_token())]))  # noqa: C419
            case Operation.OR:
                push_stack(any([pop_stack() for _ in range(next_token())]))  # noqa: C419
            case Operation.PLUS:
                push_stack(pop_stack() + pop_stack())
            case Operation.MINUS:
                push_stack(pop_stack() - pop_stack())
            case Operation.DIVIDE:
                push_stack(pop_stack() / pop_stack())
            case Operation.MULTIPLY:
                push_stack(pop_stack() * pop_stack())
            case Operation.MOD:
                push_stack(pop_stack() % pop_stack())
            case Operation.EQ:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 == var2)
            case Operation.NOT_EQ:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 != var2)
            case Operation.GT:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 > var2)
            case Operation.GT_EQ:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 >= var2)
            case Operation.LT:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 < var2)
            case Operation.LT_EQ:
                var1, var2 = unify_comparison_types(pop_stack(), pop_stack())
                push_stack(var1 <= var2)
            case Operation.LIKE:
                push_stack(like(pop_stack(), pop_stack()))
            case Operation.ILIKE:
                push_stack(like(pop_stack(), pop_stack(), re.IGNORECASE))
            case Operation.NOT_LIKE:
                push_stack(not like(pop_stack(), pop_stack()))
            case Operation.NOT_ILIKE:
                push_stack(not like(pop_stack(), pop_stack(), re.IGNORECASE))
            case Operation.IN:
                push_stack(pop_stack() in pop_stack())
            case Operation.NOT_IN:
                push_stack(pop_stack() not in pop_stack())
            case Operation.REGEX:
                args = [pop_stack(), pop_stack()]
                # TODO: swap this for re2, as used in ClairQL/ClickHouse and in the NodeJS VM
                push_stack(bool(re.search(re.compile(args[1]), args[0])))
            case Operation.NOT_REGEX:
                args = [pop_stack(), pop_stack()]
                # TODO: swap this for re2, as used in ClairQL/ClickHouse and in the NodeJS VM
                push_stack(not bool(re.search(re.compile(args[1]), args[0])))
            case Operation.IREGEX:
                args = [pop_stack(), pop_stack()]
                push_stack(bool(re.search(re.compile(args[1], re.RegexFlag.IGNORECASE), args[0])))
            case Operation.NOT_IREGEX:
                args = [pop_stack(), pop_stack()]
                push_stack(not bool(re.search(re.compile(args[1], re.RegexFlag.IGNORECASE), args[0])))
            case Operation.GET_GLOBAL:
                chain = [pop_stack() for _ in range(next_token())]
                if globals and chain[0] in globals:
                    push_stack(deepcopy(get_nested_value(globals, chain, True)))
                elif functions and chain[0] in functions:
                    push_stack(
                        new_hog_closure(
                            new_hog_callable(
                                type="stl",
                                name=chain[0],
                                arg_count=0,
                                upvalue_count=0,
                                ip=-1,
                                chunk="stl",
                            )
                        )
                    )
                elif chain[0] in STL and len(chain) == 1:
                    push_stack(
                        new_hog_closure(
                            new_hog_callable(
                                type="stl",
                                name=chain[0],
                                arg_count=STL[chain[0]].maxArgs or 0,
                                upvalue_count=0,
                                ip=-1,
                                chunk="stl",
                            )
                        )
                    )
                elif chain[0] in BYTECODE_STL and len(chain) == 1:
                    push_stack(
                        new_hog_closure(
                            new_hog_callable(
                                type="stl",
                                name=chain[0],
                                arg_count=len(BYTECODE_STL[chain[0]][0]),
                                upvalue_count=0,
                                ip=0,
                                chunk=f"stl/{chain[0]}",
                            )
                        )
                    )
                else:
                    raise ClairVMException(f"Global variable not found: {chain[0]}")
            case Operation.POP:
                pop_stack()
            case Operation.CLOSE_UPVALUE:
                stack_keep_first_elements(len(stack) - 1)
            case Operation.RETURN:
                response = pop_stack()
                last_call_frame = call_stack.pop()
                if len(call_stack) == 0 or last_call_frame is None:
                    return BytecodeResult(result=response, stdout=stdout, bytecode=bytecode)
                stack_start = last_call_frame.stack_start
                stack_keep_first_elements(stack_start)
                push_stack(response)
                frame = call_stack[-1]
                set_chunk_bytecode()
                continue  # resume the loop without incrementing frame.ip

            case Operation.GET_LOCAL:
                stack_start = 0 if not call_stack else call_stack[-1].stack_start
                push_stack(stack[next_token() + stack_start])
            case Operation.SET_LOCAL:
                stack_start = 0 if not call_stack else call_stack[-1].stack_start
                value = pop_stack()
                index = next_token() + stack_start
                stack[index] = value
                last_cost = mem_stack[index]
                mem_stack[index] = calculate_cost(value)
                mem_used += mem_stack[index] - last_cost
                max_mem_used = max(mem_used, max_mem_used)
            case Operation.GET_PROPERTY:
                property = pop_stack()
                push_stack(get_nested_value(pop_stack(), [property]))
            case Operation.GET_PROPERTY_NULLISH:
                property = pop_stack()
                push_stack(get_nested_value(pop_stack(), [property], nullish=True))
            case Operation.SET_PROPERTY:
                value = pop_stack()
                field = pop_stack()
                set_nested_value(pop_stack(), [field], value)
            case Operation.DICT:
                count = next_token()
                if count > 0:
                    elems = stack[-(count * 2) :]
                    stack = stack[: -(count * 2)]
                    mem_used -= sum(mem_stack[-(count * 2) :])
                    mem_stack = mem_stack[: -(count * 2)]
                    push_stack({elems[i]: elems[i + 1] for i in range(0, len(elems), 2)})
                else:
                    push_stack({})
            case Operation.ARRAY:
                count = next_token()
                if count > 0:
                    elems = stack[-count:]
                    stack = stack[:-count]
                    mem_used -= sum(mem_stack[-count:])
                    mem_stack = mem_stack[:-count]
                    push_stack(elems)
                else:
                    push_stack([])
            case Operation.TUPLE:
                count = next_token()
                if count > 0:
                    elems = stack[-count:]
                    stack = stack[:-count]
                    mem_used -= sum(mem_stack[-count:])
                    mem_stack = mem_stack[:-count]
                    push_stack(tuple(elems))
                else:
                    push_stack(())
            case Operation.JUMP:
                count = next_token()
                frame.ip += count
            case Operation.JUMP_IF_FALSE:
                count = next_token()
                if not pop_stack():
                    frame.ip += count
            case Operation.JUMP_IF_STACK_NOT_NULL:
                count = next_token()
                if len(stack) > 0 and stack[-1] is not None:
                    frame.ip += count
            case Operation.DECLARE_FN:
                # DEPRECATED
                name = next_token()
                arg_len = next_token()
                body_len = next_token()
                declared_functions[name] = (frame.ip + 1, arg_len)
                frame.ip += body_len
            case Operation.CALLABLE:
                name = next_token()  # TODO: do we need it? it could change as the variable is reassigned
                arg_count = next_token()
                upvalue_count = next_token()
                body_length = next_token()
                push_stack(
                    new_hog_callable(
                        type="local",
                        name=name,
                        chunk=frame.chunk,
                        arg_count=arg_count,
                        upvalue_count=upvalue_count,
                        ip=frame.ip + 1,
                    )
                )
                frame.ip += body_length
            case Operation.CLOSURE:
                closure_callable = pop_stack()
                closure = new_hog_closure(closure_callable)
                stack_start = frame.stack_start
                upvalue_count = next_token()
                if upvalue_count != closure_callable["upvalueCount"]:
                    raise ClairVMException(
                        f"Invalid upvalue count. Expected {closure_callable['upvalueCount']}, got {upvalue_count}"
                    )
                for _ in range(closure_callable["upvalueCount"]):
                    is_local, index = next_token(), next_token()
                    if is_local:
                        closure["upvalues"].append(capture_upvalue(stack_start + index)["id"])
                    else:
                        closure["upvalues"].append(frame.closure["upvalues"][index])
                push_stack(closure)
            case Operation.GET_UPVALUE:
                index = next_token()
                closure = frame.closure
                if index >= len(closure["upvalues"]):
                    raise ClairVMException(f"Invalid upvalue index: {index}")
                upvalue = upvalues_by_id[closure["upvalues"][index]]
                if not is_hog_upvalue(upvalue):
                    raise ClairVMException(f"Invalid upvalue: {upvalue}")
                if upvalue["closed"]:
                    push_stack(upvalue["value"])
                else:
                    push_stack(stack[upvalue["location"]])
            case Operation.SET_UPVALUE:
                index = next_token()
                closure = frame.closure
                if index >= len(closure["upvalues"]):
                    raise ClairVMException(f"Invalid upvalue index: {index}")
                upvalue = upvalues_by_id[closure["upvalues"][index]]
                if not is_hog_upvalue(upvalue):
                    raise ClairVMException(f"Invalid upvalue: {upvalue}")
                if upvalue["closed"]:
                    upvalue["value"] = pop_stack()
                else:
                    stack[upvalue["location"]] = pop_stack()
            case Operation.CALL_GLOBAL:
                check_timeout()
                name = next_token()
                arg_count = next_token()
                # This is for backwards compatibility. We use a closure on the stack with local functions now.
                if name in declared_functions:
                    func_ip, arg_len = declared_functions[name]
                    frame.ip += 1  # advance for when we return
                    if arg_len > arg_count:
                        for _ in range(arg_len - arg_count):
                            push_stack(None)
                    frame = CallFrame(
                        ip=func_ip,
                        chunk=frame.chunk,
                        stack_start=len(stack) - arg_len,
                        arg_len=arg_len,
                        closure=new_hog_closure(
                            new_hog_callable(
                                type="local",
                                name=name,
                                arg_count=arg_len,
                                upvalue_count=0,
                                ip=func_ip,
                                chunk=frame.chunk,
                            )
                        ),
                    )
                    call_stack.append(frame)
                    continue  # resume the loop without incrementing frame.ip
                else:
                    if functions is not None and name in functions:
                        if version == 0:
                            args = [pop_stack() for _ in range(arg_count)]
                        else:
                            args = stack_keep_first_elements(len(stack) - arg_count)
                        push_stack(functions[name](*args))
                    elif name in STL:
                        if version == 0:
                            args = [pop_stack() for _ in range(arg_count)]
                        else:
                            args = stack_keep_first_elements(len(stack) - arg_count)
                        push_stack(STL[name].fn(args, team, stdout, timeout.total_seconds()))
                    elif name in BYTECODE_STL:
                        arg_names = BYTECODE_STL[name][0]
                        if len(arg_names) != arg_count:
                            raise ClairVMException(f"Function {name} requires exactly {len(arg_names)} arguments")
                        frame.ip += 1  # advance for when we return
                        frame = CallFrame(
                            ip=0,
                            chunk=f"stl/{name}",
                            stack_start=len(stack) - arg_count,
                            arg_len=arg_count,
                            closure=new_hog_closure(
                                new_hog_callable(
                                    type="stl",
                                    name=name,
                                    arg_count=arg_count,
                                    upvalue_count=0,
                                    ip=0,
                                    chunk=f"stl/{name}",
                                )
                            ),
                        )
                        set_chunk_bytecode()
                        call_stack.append(frame)
                        continue  # resume the loop without incrementing frame.ip
                    else:
                        raise ClairVMException(f"Unsupported function call: {name}")
            case Operation.CALL_LOCAL:
                check_timeout()
                closure = pop_stack()
                if not isinstance(closure, dict) or closure.get("__hogClosure__") is None:
                    raise ClairVMException(f"Invalid closure: {closure}")
                callable = closure.get("callable")
                if not isinstance(callable, dict) or callable.get("__hogCallable__") is None:
                    raise ClairVMException(f"Invalid callable: {callable}")
                args_length = next_token()
                if args_length > MAX_FUNCTION_ARGS_LENGTH:
                    raise ClairVMException("Too many arguments")

                if callable.get("__hogCallable__") == "local":
                    if callable["argCount"] > args_length:
                        # TODO: specify minimum required arguments somehow
                        for _ in range(callable["argCount"] - args_length):
                            push_stack(None)
                    elif callable["argCount"] < args_length:
                        raise ClairVMException(
                            f"Too many arguments. Passed {args_length}, expected {callable['argCount']}"
                        )
                    frame.ip += 1  # advance for when we return
                    frame = CallFrame(
                        ip=callable["ip"],
                        chunk=callable["chunk"],
                        stack_start=len(stack) - callable["argCount"],
                        arg_len=callable["argCount"],
                        closure=closure,
                    )
                    set_chunk_bytecode()
                    call_stack.append(frame)
                    continue  # resume the loop without incrementing frame.ip

                elif callable.get("__hogCallable__") == "stl":
                    if callable["name"] not in STL:
                        raise ClairVMException(f"Unsupported function call: {callable['name']}")
                    stl_fn = STL[callable["name"]]
                    if stl_fn.minArgs is not None and args_length < stl_fn.minArgs:
                        raise ClairVMException(
                            f"Function {callable['name']} requires at least {stl_fn.minArgs} arguments"
                        )
                    if stl_fn.maxArgs is not None and args_length > stl_fn.maxArgs:
                        raise ClairVMException(f"Function {callable['name']} requires at most {stl_fn.maxArgs} arguments")
                    if version == 0:
                        args = [pop_stack() for _ in range(args_length)]
                    else:
                        args = list(reversed([pop_stack() for _ in range(args_length)]))
                        if stl_fn.maxArgs is not None and len(args) < stl_fn.maxArgs:
                            args = [*args, *([None] * (stl_fn.maxArgs - len(args)))]
                    push_stack(stl_fn.fn(args, team, stdout, timeout.total_seconds()))

                elif callable.get("__hogCallable__") == "async":
                    raise ClairVMException("Async functions are not supported")

                else:
                    raise ClairVMException("Invalid callable")

            case Operation.TRY:
                throw_stack.append(
                    ThrowFrame(
                        call_stack_len=len(call_stack), stack_len=len(stack), catch_ip=frame.ip + 1 + next_token()
                    )
                )
            case Operation.POP_TRY:
                if throw_stack:
                    throw_stack.pop()
                else:
                    raise ClairVMException("Invalid operation POP_TRY: no try block to pop")
            case Operation.THROW:
                exception = pop_stack()
                if not is_hog_error(exception):
                    raise ClairVMException("Can not throw: value is not of type Error")
                if throw_stack:
                    last_throw = throw_stack.pop()
                    call_stack_len, stack_len, catch_ip = (
                        last_throw.call_stack_len,
                        last_throw.stack_len,
                        last_throw.catch_ip,
                    )
                    stack_keep_first_elements(stack_len)
                    call_stack = call_stack[0:call_stack_len]
                    push_stack(exception)
                    frame = call_stack[-1]
                    set_chunk_bytecode()
                    frame.ip = catch_ip
                    continue
                else:
                    raise UncaughtClairVMException(
                        type=exception.get("type"),
                        message=exception.get("message"),
                        payload=exception.get("payload"),
                    )
            case _:
                raise ClairVMException(
                    f'Unexpected node while running bytecode in chunk "{frame.chunk}": {chunk_bytecode[frame.ip]}'
                )

        frame.ip += 1
    if debug:
        debugger(symbol, bytecode, colored_bytecode, frame.ip, stack, call_stack, throw_stack)
    if len(stack) > 1:
        raise ClairVMException("Invalid bytecode. More than one value left on stack")
    if len(stack) == 1:
        result = pop_stack()
    return BytecodeResult(result=result, stdout=stdout, bytecode=bytecode)