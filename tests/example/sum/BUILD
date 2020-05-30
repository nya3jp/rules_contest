package(default_visibility = ["//tests/example/sum:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "jinja2_template",
    "markdown",
    "py_yaml_library",
)

buildifier_test()

py_yaml_library(
    name = "constraints_py",
    src = "constraints.yaml",
)

jinja2_template(
    name = "statement_subst",
    srcs = ["statement.md"],
    dataset = "//tests/example/sum/judge:dataset",
    files = ["//tests/example/sum/judge:sample_outputs"],
    vars = ["constraints.yaml"],
)

markdown(
    name = "statement",
    src = ":statement_subst",
)
