package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

py_library(
    name = "markupsafe",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    visibility = ["//third_party/jinja2:__subpackages__"],
)
