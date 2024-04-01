package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_generate")

lint_all()

py_binary(
    name = "generator",
    srcs = ["generator.py"],
    data = [":generator.data"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = ["@bazel_tools//tools/python/runfiles"],
)

dataset_generate(
    name = "dataset",
    cmd = "${EXEC} --passphrase='a b c' --mode=default",
    exec = ":generator",
)

dataset_generate(
    name = "empty",
    cmd = "${EXEC} --passphrase='a b c' --mode=empty",
    exec = ":generator",
)

py_test(
    name = "dataset_generate_test",
    srcs = ["dataset_generate_test.py"],
    data = [
        ":dataset",
        ":empty",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
)
