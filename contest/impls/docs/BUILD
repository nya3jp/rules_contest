package(default_visibility = ["//visibility:private"])

load("//contest/impls/lint:defs.bzl", "buildifier_test")
load("@io_bazel_stardoc//stardoc:stardoc.bzl", "stardoc")

buildifier_test()

stardoc(
    name = "reference",
    out = "reference.md",
    input = "//contest:defs.bzl",
)
