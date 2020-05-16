package(default_visibility=["//visibility:public"])

cc_binary(
    name = "cpp_WA",
    srcs = ["cpp_WA.cc"],
)

solution_test(
    name = "cpp_WA_test",
    solution = ":cpp_WA",
    judge = "//ab/judge",
    judge_args = ["--expect=reject_any"]
)
