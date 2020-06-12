package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")
load("//contest:defs.bzl", "dataset_merge", "simple_judge")

buildifier_test()

pycodestyle_test(
    name = "pycodestyle_test",
    srcs = glob(["*.py"]),
)

dataset_merge(
    name = "dataset",
    files = glob(["*.in"]),
)

py_binary(
    name = "comparator",
    srcs = ["comparator.py"],
    data = [":data.txt"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

simple_judge(
    name = "judge",
    comparator = ":comparator",
    comparator_cmd = "${EXEC} --input_file=${INPUT_DIR}/${TESTCASE}.in --output_file=${OUTPUT_FILE}",
    dataset = ":dataset",
)

py_binary(
    name = "good_solution",
    srcs = ["good_solution.py"],
    data = [":data.txt"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "half_solution",
    srcs = ["half_solution.py"],
    data = [":data.txt"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "bad_solution",
    srcs = ["bad_solution.py"],
    data = [":data.txt"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_test(
    name = "simple_judge_test",
    srcs = ["simple_judge_test.py"],
    data = [
        ":bad_solution",
        ":good_solution",
        ":half_solution",
        ":judge",
        ":results_golden.json",
    ],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)