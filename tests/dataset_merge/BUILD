package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge")

lint_all()

dataset_merge(
    name = "dataset1",
    files = [
        "data1.in",
        "data2.in",
    ],
)

dataset_merge(
    name = "dataset2",
    files = ["data3.ans"],
)

dataset_merge(
    name = "dataset",
    datasets = [
        ":dataset1",
        ":dataset2",
    ],
    files = ["data3.in"],
)

dataset_merge(
    name = "empty",
)

py_test(
    name = "dataset_merge_test",
    srcs = ["dataset_merge_test.py"],
    data = [
        ":dataset",
        ":empty",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
)
