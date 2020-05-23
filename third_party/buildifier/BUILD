package(default_visibility=["//visibility:private"])

genrule(
    name = "buildifier_cp",
    outs = ["buildifier"],
    srcs = select({
        "@bazel_tools//src/conditions:linux_x86_64": ["@buildifier_prebuilt_linux//file"],
        "@bazel_tools//src/conditions:darwin": ["@buildifier_prebuilt_mac//file"],
        "@bazel_tools//src/conditions:darwin_x86_64": ["@buildifier_prebuilt_mac//file"],
        "@bazel_tools//src/conditions:windows": ["@buildifier_prebuilt_windows//file"],
    }),
    cmd = "cp $< $@",
    visibility = ["//:__subpackages__"],
)
