package(default_visibility = ["//visibility:private"])

load("//lint:defs.bzl", "lint_all")

lint_all()

genrule(
    name = "buildifier_cp",
    srcs = select({
        "@bazel_tools//src/conditions:linux_x86_64": ["@buildifier_prebuilt_linux_amd64//file"],
        "@bazel_tools//src/conditions:darwin": ["@buildifier_prebuilt_darwin_amd64//file"],
        "@bazel_tools//src/conditions:windows": ["@buildifier_prebuilt_windows_amd64//file"],
    }),
    outs = ["buildifier"],
    cmd = "cp $< $@",
    visibility = ["//:__subpackages__"],
)
