package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge")
load("//contest:experimental_defs.bzl", "domjudge_package")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob([
        "*.in",
        "*.ans",
    ]),
)

domjudge_package(
    name = "problem",
    dataset = ":dataset",
    domjudge_metadata = ":domjudge-problem.ini",
    icpc_metadata = ":problem.yaml",
    statements = [":statement.html"],
)
