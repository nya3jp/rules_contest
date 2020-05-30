package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "zipp",
    srcs = ["zipp.py"],
    imports = ["."],
    visibility = ["//third_party/importlib_metadata:__subpackages__"],
)
