package(default_visibility = ["//tests/example/sum:__subpackages__"])

load("//lint:defs.bzl", "lint_all")
load(
    "//contest:defs.bzl",
    "solution_test",
)

lint_all()

cc_binary(
    name = "cpp",
    srcs = ["cpp.cc"],
)

solution_test(
    name = "cpp_test",
    judge = "//tests/example/sum/judge",
    solution = ":cpp",
)
