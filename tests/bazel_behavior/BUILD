package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_test(
    name = "args_test",
    srcs = ["args_test.py"],
    args = [
        "a b",
        "\"c d\" 'e f'",
        " g  h  ",
        "   ",
        "--",
        "",
        "\"\"",
        "''",
        "\\\"\\\"",
        "\\'\\'",
        "$$HOME",
        "|| true",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
)
