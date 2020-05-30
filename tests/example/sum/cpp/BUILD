package(default_visibility = ["//tests/example/sum:__subpackages__"])

load("//contest/impls/lint:defs.bzl", "buildifier_test")
load(
    "//contest:defs.bzl",
    "solution_test",
)

buildifier_test()

cc_binary(
    name = "cpp",
    srcs = ["cpp.cc"],
)

solution_test(
    name = "cpp_test",
    judge = "//tests/example/sum/judge",
    solution = ":cpp",
)
