package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test", "pycodestyle_test")

buildifier_test()

exports_files(["defs.bzl"])

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
