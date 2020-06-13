package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_library(
    name = "jinja2",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//contest:__subpackages__"],
    deps = ["//third_party/markupsafe"],
)
