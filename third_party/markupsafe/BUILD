package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "markupsafe",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//third_party/jinja2:__subpackages__"],
)
