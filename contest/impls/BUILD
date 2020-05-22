package(default_visibility = ["//visibility:private"])

py_binary(
    name = "dataset_generate",
    srcs = ["dataset_generate.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "dataset_derive",
    srcs = ["dataset_derive.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "dataset_merge",
    srcs = ["dataset_merge.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "dataset_test",
    srcs = ["dataset_test.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "dataset_test_wrapper_generator",
    srcs = ["dataset_test_wrapper_generator.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
)

py_binary(
    name = "simple_judge",
    srcs = ["simple_judge.py"],
    srcs_version = "PY3",
    deps = [":datasets"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "simple_judge_wrapper_generator",
    srcs = ["simple_judge_wrapper_generator.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
)

py_binary(
    name = "solution_test_wrapper_generator",
    srcs = ["solution_test_wrapper_generator.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
)

py_library(
    name = "datasets",
    srcs = ["datasets.py"],
    srcs_version = "PY3",
)

py_binary(
    name = "jinja2_template",
    srcs = ["jinja2_template.py"],
    srcs_version = "PY3",
    deps = [
        ":datasets",
        "//third_party/jinja2",
        "//third_party/yaml",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "render_markdown",
    srcs = ["render_markdown.py"],
    srcs_version = "PY3",
    deps = [
        "//third_party/markdown",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "cc_yaml_library",
    srcs = ["cc_yaml_library.py"],
    srcs_version = "PY3",
    deps = [
        "//third_party/yaml",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "py_yaml_library",
    srcs = ["py_yaml_library.py"],
    srcs_version = "PY3",
    deps = [
        "//third_party/yaml",
    ],
    visibility = ["//visibility:public"],
)
