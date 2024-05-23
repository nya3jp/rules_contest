package(default_visibility = ["//sum:__subpackages__"])

load(
    "@rules_contest//contest:defs.bzl",
    "jinja2_template",
    "markdown",
    "py_yaml_library",
)

py_yaml_library(
    name = "constraints_py",
    src = "constraints.yaml",
)

jinja2_template(
    name = "statement_subst",
    srcs = ["statement.md"],
    dataset = "//sum/judge:dataset",
    files = ["//sum/judge:sample_outputs"],
    vars = ["constraints.yaml"],
)

markdown(
    name = "statement",
    src = ":statement_subst",
)
