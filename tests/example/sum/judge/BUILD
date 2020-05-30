package(default_visibility = ["//tests/example/sum:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "dataset_derive",
    "dataset_generate",
    "dataset_merge",
    "dataset_test",
    "sample_test",
    "simple_judge",
)

buildifier_test()

py_binary(
    name = "generator",
    srcs = ["generator.py"],
    deps = ["//tests/example/sum:constraints_py"],
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
    exec = "//tests/example/sum/cpp",
)

simple_judge(
    name = "judge",
    dataset = ":dataset",
)

py_binary(
    name = "validator",
    srcs = ["validator.py"],
    deps = ["//tests/example/sum:constraints_py"],
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
