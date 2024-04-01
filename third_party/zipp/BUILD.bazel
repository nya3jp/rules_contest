package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_library(
    name = "zipp",
    srcs = ["zipp.py"],
    imports = ["."],
    visibility = ["//third_party/importlib_metadata:__subpackages__"],
)
