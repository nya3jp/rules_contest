package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge", "interactive_judge")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob(["*.in"]),
)

cc_binary(
    name = "server",
    srcs = ["server.c"],
    copts = ["-Wno-unused-result"],
)

py_binary(
    name = "server_with_runfiles",
    srcs = ["server_with_runfiles.py"],
    data = [":server.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

interactive_judge(
    name = "judge",
    case_timeout = 1,
    dataset = ":dataset",
    exec = ":server",
)

interactive_judge(
    name = "judge_with_runfiles",
    dataset = ":dataset",
    exec = ":server_with_runfiles",
)

cc_binary(
    name = "solution_good",
    srcs = ["solution_good.c"],
    copts = ["-Wno-unused-result"],
)

cc_binary(
    name = "solution_half",
    srcs = ["solution_half.c"],
    copts = ["-Wno-unused-result"],
)

cc_binary(
    name = "solution_bad",
    srcs = ["solution_bad.c"],
    copts = ["-Wno-unused-result"],
)

cc_binary(
    name = "solution_slow",
    srcs = ["solution_slow.c"],
    copts = ["-Wno-unused-result"],
)

py_binary(
    name = "solution_with_runfiles",
    srcs = ["solution_with_runfiles.py"],
    data = [":solution.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

py_test(
    name = "interactive_judge_test",
    srcs = ["interactive_judge_test.py"],
    data = [
        ":judge",
        ":judge_with_runfiles",
        ":results_golden.json",
        ":solution_bad",
        ":solution_good",
        ":solution_half",
        ":solution_slow",
        ":solution_with_runfiles",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)
