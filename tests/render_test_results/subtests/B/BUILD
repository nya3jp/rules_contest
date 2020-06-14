package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")
load("//contest:defs.bzl", "dataset_merge", "simple_judge", "solution_test")

lint_all()

dataset_merge(
    name = "dataset",
    files = glob([
        "*.in",
        "*.ans",
    ]),
)

simple_judge(
    name = "judge",
    dataset = ":dataset",
)

cc_binary(
    name = "solution",
    srcs = ["solution.c"],
)

solution_test(
    name = "solution_accept_all_test",
    judge = ":judge",
    solution = ":solution",
    tags = [
        "exclusive",
        "manual",
    ],
)

solution_test(
    name = "solution_reject_any_test",
    judge = ":judge",
    judge_args = ["--expect=reject_any"],
    solution = ":solution",
    tags = [
        "exclusive",
        "manual",
    ],
)
