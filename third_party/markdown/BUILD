package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "markdown",
    srcs = glob(["**/*.py"]),
    data = glob(["*.egg-info/*"]),
    imports = ["."],
    visibility = ["//contest:__subpackages__"],
    deps = ["//third_party/importlib_metadata"],
)
