package(default_visibility=["//visibility:private"])

py_library(
    name = "importlib_metadata",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    data = glob(["*.egg-info/*"]),
    deps = ["//third_party/zipp"],
    visibility = ["//third_party/markdown:__subpackages__"],
)
