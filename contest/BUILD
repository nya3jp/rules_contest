package(default_visibility = ["//visibility:private"])

sh_binary(
    name = "exact_comparator",
    srcs = ["exact_comparator.sh"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "fake_coverage_report_generator",
    srcs = ["fake_coverage_report_generator.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "run_solution_tests",
    srcs = ["run_solution_tests.py"],
)
