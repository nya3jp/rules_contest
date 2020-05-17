package(default_visibility=["//visibility:public"])

markdown(
    name = "statement",
    src = ":statement_subst",
)

jinja2_template(
    name = "statement_subst",
    srcs = ["statement.md"],
    vars = ["constraints.yaml"],
    datasets = ["//ab/judge:dataset"],
)

py_yaml_library(
    name = "constraints_py",
    src = "constraints.yaml",
)
