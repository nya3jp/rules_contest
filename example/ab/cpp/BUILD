package(default_visibility=["//visibility:public"])

cc_binary(
    name = "cpp",
    srcs = ["cpp.cc"],
)

solution_test(
    name = "cpp_test",
    solution = ":cpp",
    judge = "//ab/judge",
)
