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
    srcs_version = "PY3",
)
