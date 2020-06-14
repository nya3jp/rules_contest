package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge", "interactive_judge")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob(["*.in"]),
)

py_binary(
    name = "server",
    srcs = ["server.py"],
    data = [":server.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
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

interactive_judge(
    name = "judge",
    cmd = "${EXEC} ${INPUT_DIR}/${TESTCASE}.in",
    dataset = ":dataset",
    exec = ":server",
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
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)
