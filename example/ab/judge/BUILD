package(default_visibility=["//visibility:public"])

simple_judge(
    name = "judge",
    datasets = [":dataset"],
)

dataset_derive(
    name = "dataset",
    datasets = glob(["*.in", "*.diff"]) + [":generated"],
    exec = "//ab/cpp",
    input_extension = "in",
    output_extension = "diff",
)

dataset_generate(
    name = "generated",
    exec = ":generator",
)

py_binary(
    name = "generator",
    srcs = ["generator.py"],
    deps = ["//ab:constraints_py"],
)

py_binary(
    name = "validator",
    srcs = ["validator.py"],
    deps = ["//ab:constraints_py"],
)

dataset_test(
    name = "dataset_test",
    exec = ":validator",
    datasets = [":dataset"],
)
