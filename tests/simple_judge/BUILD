package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge", "simple_judge")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob(["*.in"]),
)

py_binary(
    name = "comparator",
    srcs = ["comparator.py"],
    data = [":comparator.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

simple_judge(
    name = "judge",
    case_timeout = 1,
    comparator = ":comparator",
    comparator_cmd = "${EXEC} --input_file=${INPUT_DIR}/${TESTCASE}.in --output_file=${OUTPUT_FILE}",
    dataset = ":dataset",
)

py_binary(
    name = "good_solution",
    srcs = ["good_solution.py"],
    data = [":solution.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "half_solution",
    srcs = ["half_solution.py"],
    data = [":solution.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "bad_solution",
    srcs = ["bad_solution.py"],
    data = [":solution.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "long_solution",
    srcs = ["long_solution.py"],
    python_version = "PY3",
    srcs_version = "PY3",
)

py_test(
    name = "simple_judge_test",
    srcs = ["simple_judge_test.py"],
    data = [
        ":bad_solution",
        ":good_solution",
        ":half_solution",
        ":judge",
        ":long_solution",
        ":results_golden.json",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)
