package(default_visibility = ["//tests/example/sqrt:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "jinja2_template",
    "markdown",
    "py_yaml_library",
)
load("//contest:experimental_defs.bzl", "domjudge_package")

buildifier_test()

py_yaml_library(
    name = "constraints_py",
    src = "constraints.yaml",
)

jinja2_template(
    name = "statement_subst",
    srcs = ["statement.md"],
    dataset = "//tests/example/sqrt/judge:dataset",
    files = ["//tests/example/sqrt/judge:sample_outputs"],
    vars = ["constraints.yaml"],
)

markdown(
    name = "statement",
    src = ":statement_subst",
)

domjudge_package(
    name = "sqrt",
    dataset = "//tests/example/sqrt/judge:dataset",
    domjudge_metadata = "domjudge-problem.ini",
    icpc_metadata = "problem.yaml",
    statements = [":statement"],
)
