package(default_visibility = ["//tests/example/sqrt:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "solution_test",
)

buildifier_test()

py_binary(
    name = "python",
    srcs = ["python.py"],
    srcs_version = "PY3",
)

solution_test(
    name = "python_test",
    judge = "//tests/example/sqrt/judge",
    solution = ":python",
)
