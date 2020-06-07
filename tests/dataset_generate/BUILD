load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")
load("//contest:defs.bzl", "dataset_generate")

buildifier_test()

pycodestyle_test(
    name = "pycodestyle_test",
    srcs = glob(["*.py"]),
)

py_binary(
    name = "generator",
    srcs = ["generator.py"],
    srcs_version = "PY3",
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
    srcs_version = "PY3",
)
