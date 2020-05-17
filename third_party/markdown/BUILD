package(default_visibility=["//visibility:private"])

py_library(
    name = "markdown",
    srcs = glob(["**/*.py"]),
    imports = ["."],
    data = glob(["*.egg-info/*"]),
    deps = ["//third_party/importlib_metadata"],
    visibility = ["//contest:__subpackages__"],
)
