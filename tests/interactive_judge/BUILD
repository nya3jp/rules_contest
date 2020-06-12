package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")
load("//contest:defs.bzl", "dataset_merge", "interactive_judge")

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
    name = "peer",
    srcs = ["peer.py"],
    data = [":peer.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "good_solution",
    srcs = ["good_solution.py"],
    data = [":solution.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "half_solution",
    srcs = ["half_solution.py"],
    data = [":solution.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_binary(
    name = "bad_solution",
    srcs = ["bad_solution.py"],
    data = [":solution.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

interactive_judge(
    name = "judge",
    cmd = "${EXEC} ${INPUT_DIR}/${TESTCASE}.in",
    dataset = ":dataset",
    exec = ":peer",
)

py_test(
    name = "interactive_judge_test",
    srcs = ["interactive_judge_test.py"],
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