package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "importlib_metadata",
    srcs = glob(["**/*.py"]),
    data = glob(["*.egg-info/*"]),
    imports = ["."],
    visibility = ["//third_party/markdown:__subpackages__"],
    deps = ["//third_party/zipp"],
)
