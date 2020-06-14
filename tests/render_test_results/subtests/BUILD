package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

sh_test(
    name = "good_test",
    srcs = ["good_test.sh"],
    tags = [
        "exclusive",
        "manual",
    ],
)

sh_test(
    name = "bad_test",
    srcs = ["bad_test.sh"],
    tags = [
        "exclusive",
        "manual",
    ],
)
