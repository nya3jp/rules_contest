package(default_visibility = ["//tests/example/sum:__subpackages__"])

load("//lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "solution_test",
)

buildifier_test()

cc_binary(
    name = "cpp_WA",
    srcs = ["cpp_WA.cc"],
)

solution_test(
    name = "cpp_WA_test",
    judge = "//tests/example/sum/judge",
    judge_args = ["--expect=reject_any"],
    solution = ":cpp_WA",
)
