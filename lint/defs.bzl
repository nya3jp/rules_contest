def pycodestyle_test(name, srcs, **kwargs):
    args = ["--max-line-length=160"]
    args.extend(["$(rootpath " + src + ")" for src in srcs])
    native.py_test(
        name = name,
        srcs = ["//third_party/pycodestyle:pycodestyle.py"],
        main = "//third_party/pycodestyle:pycodestyle.py",
        data = srcs,
        args = args,
        **kwargs
    )

def buildifier_test(name = "buildifier_test", srcs = None, type = "auto", **kwargs):
    if not srcs:
        srcs = native.glob(["WORKSPACE", "WORKSPACE.bazel", "BUILD", "BUILD.bazel", "*.bzl"])
    args = ["-mode=diff", "-type=" + type]
    args.extend(["$(rootpath " + src + ")" for src in srcs])
    native.sh_test(
        name = name,
        srcs = ["//third_party/buildifier"],
        data = srcs,
        args = args,
        **kwargs
    )
