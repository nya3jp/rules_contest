package(default_visibility = ["//contest/impls:__subpackages__"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_library(
    name = "datasets",
    srcs = ["datasets.py"],
    srcs_version = "PY3",
)

py_test(
    name = "datasets_test",
    srcs = ["datasets_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [":datasets"],
)

py_library(
    name = "exec_util",
    srcs = ["exec_util.py"],
    srcs_version = "PY3",
)

py_library(
    name = "judge_common",
    srcs = ["judge_common.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
)
