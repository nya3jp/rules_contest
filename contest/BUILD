package(default_visibility = ["//visibility:private"])

load("//contest/impls/lint:defs.bzl", "pycodestyle_test")

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
    name = "render_test_results",
    srcs = ["render_test_results.py"],
    data = ["test_results.md"],
    deps = ["//third_party/jinja2"],
)

pycodestyle_test(
    name = "pycodestyle_test",
    srcs = glob(["*.py"]),
)
