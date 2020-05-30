package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

py_library(
    name = "jinja2",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//contest:__subpackages__"],
    deps = ["//third_party/markupsafe"],
)
