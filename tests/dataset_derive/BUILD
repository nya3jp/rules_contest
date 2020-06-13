package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")
load("//contest:defs.bzl", "dataset_derive", "dataset_merge")

buildifier_test()

pycodestyle_test(
    name = "pycodestyle_test",
    srcs = glob(["*.py"]),
)

py_binary(
    name = "deriver",
    srcs = ["deriver.py"],
    data = [":deriver.data"],
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

dataset_merge(
    name = "inputs",
    files = glob(["*.in"]),
)

dataset_derive(
    name = "dataset1",
    dataset = ":inputs",
    exec = ":deriver",
)

dataset_derive(
    name = "dataset2",
    cmd = "${EXEC} --multiplier=111 < ${INPUT_DIR}/${TESTCASE}.in > ${OUTPUT_DIR}/${TESTCASE}.ans",
    dataset = ":inputs",
    exec = ":deriver",
)

py_test(
    name = "dataset_merge_test",
    srcs = ["dataset_merge_test.py"],
    data = [
        ":dataset1",
        ":dataset2",
    ],
    srcs_version = "PY3",
)
