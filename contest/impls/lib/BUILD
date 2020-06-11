package(default_visibility = ["//contest/impls:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")

buildifier_test()

pycodestyle_test(
    name = "pycodestyle_test",
    srcs = glob(["*.py"]),
)

py_library(
    name = "datasets",
    srcs = ["datasets.py"],
    srcs_version = "PY3",
)

py_library(
    name = "exec_util",
    srcs = ["exec_util.py"],
    srcs_version = "PY3",
)
