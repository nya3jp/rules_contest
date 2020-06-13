package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge", "dataset_test")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob(["*.txt"]),
)

py_binary(
    name = "validator",
    srcs = ["validator.py"],
    data = [":validator.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

dataset_test(
    name = "stdin_test",
    cmd = "${EXEC} < ${INPUT_DIR}/${TESTCASE}.txt",
    dataset = ":dataset",
    exec = ":validator",
)

dataset_test(
    name = "file_test",
    cmd = "${EXEC} ${INPUT_DIR}/${TESTCASE}.txt",
    dataset = ":dataset",
    exec = ":validator",
)
