package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "buildifier_test")

buildifier_test()

genrule(
    name = "buildifier_cp",
    srcs = select({
        "@bazel_tools//src/conditions:linux_x86_64": ["@buildifier_prebuilt_linux//file"],
        "@bazel_tools//src/conditions:darwin": ["@buildifier_prebuilt_mac//file"],
        "@bazel_tools//src/conditions:darwin_x86_64": ["@buildifier_prebuilt_mac//file"],
        "@bazel_tools//src/conditions:windows": ["@buildifier_prebuilt_windows//file"],
    }),
    outs = ["buildifier"],
    cmd = "cp $< $@",
    visibility = ["//:__subpackages__"],
)
