package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "yaml",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//:__subpackages__"],
)
