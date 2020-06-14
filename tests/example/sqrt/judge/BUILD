package(default_visibility = ["//tests/example/sqrt:__subpackages__"])

load("//lint:defs.bzl", "lint_all")
load(
    "//contest:defs.bzl",
    "dataset_derive",
    "dataset_generate",
    "dataset_merge",
    "dataset_test",
    "sample_test",
    "simple_judge",
)

lint_all()

py_binary(
    name = "generator",
    srcs = ["generator.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["//tests/example/sqrt:constraints_py"],
)

dataset_generate(
    name = "inputs_generated",
    exec = ":generator",
)

dataset_merge(
    name = "inputs",
    datasets = [":inputs_generated"],
    files = glob(["*.in"]),
)

dataset_derive(
    name = "dataset",
    dataset = ":inputs",
    exec = "//tests/example/sqrt/python",
)

py_binary(
    name = "comparator",
    srcs = ["comparator.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["//tests/example/sqrt:constraints_py"],
)

simple_judge(
    name = "judge",
    comparator = ":comparator",
    dataset = ":dataset",
)

py_binary(
    name = "validator",
    srcs = ["validator.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["//tests/example/sqrt:constraints_py"],
)

dataset_test(
    name = "dataset_test",
    dataset = ":dataset",
    exec = ":validator",
)

filegroup(
    name = "sample_outputs",
    srcs = glob(["*.out"]),
)

sample_test(
    name = "sample_test",
    files = [":sample_outputs"],
    judge = ":judge",
)
