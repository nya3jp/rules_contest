package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_library(
    name = "yaml",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//:__subpackages__"],
)
