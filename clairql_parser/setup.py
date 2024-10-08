from setuptools import setup, Extension
import platform

system = platform.system()
if system not in ("Darwin", "Linux"):
    raise Exception("Only Linux and macOS are supported by clairql_parser")

is_macos = system == "Darwin"
homebrew_location = "/opt/homebrew" if platform.machine() == "arm64" else "/usr/local"

module = Extension(
    "clairql_parser",
    sources=[
        "ClairQLLexer.cpp",
        "ClairQLParser.cpp",
        "ClairQLParserBaseVisitor.cpp",
        "ClairQLParserVisitor.cpp",
        "error.cpp",
        "string.cpp",
        "parser.cpp",
    ],
    include_dirs=[
        f"{homebrew_location}/include/",
        f"{homebrew_location}/include/antlr4-runtime/",
    ]
    if is_macos
    else ["/usr/include/", "/usr/include/antlr4-runtime/"],
    library_dirs=[f"{homebrew_location}/lib/"] if is_macos else ["/usr/lib/", "/usr/lib64/"],
    libraries=["antlr4-runtime"],
    extra_compile_args=["-std=c++20"],
)

setup(
    name="clairql_parser",
    version="1.0.45",
    url="https://github.com/ClairView/clairview/tree/master/clairql_parser",
    author="ClairView Inc.",
    author_email="developers@clairview.com",
    maintainer="ClairView Inc.",
    maintainer_email="hey@clairview.com",
    description="ClairQL parser for internal ClairView use",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"clairql_parser": ["__init__.pyi", "py.typed"]},
    ext_modules=[module],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
