#pragma once

#include <stdexcept>
#include <string>

#define ERROR_CLASS_DEFINITION(NAME, BASE)                               \
  class NAME : public BASE {                                             \
   public:                                                               \
    size_t start;                                                        \
    size_t end;                                                          \
    explicit NAME(const std::string& message, size_t start, size_t end); \
    explicit NAME(const char* message, size_t start, size_t end);        \
    explicit NAME(const std::string& message);                           \
    explicit NAME(const char* message);                                  \
  };

ERROR_CLASS_DEFINITION(TorQLError, std::runtime_error)

// The input does not conform to TorQL syntax.
ERROR_CLASS_DEFINITION(SyntaxError, TorQLError)

// This feature isn't implemented in TorQL (yet).
ERROR_CLASS_DEFINITION(NotImplementedError, TorQLError)

// An internal problem in the parser layer.
ERROR_CLASS_DEFINITION(ParsingError, TorQLError)

// Python runtime errored out somewhere - this means we must use the error it's already raised.
class PyInternalError : public std::exception {
 public:
  PyInternalError();
};
