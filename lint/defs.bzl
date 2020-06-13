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

def buildifier_test(name, srcs, type = "auto", **kwargs):
    args = ["-mode=diff", "-type=" + type]
    args.extend(["$(rootpath " + src + ")" for src in srcs])
    native.sh_test(
        name = name,
        srcs = ["//third_party/buildifier"],
        data = srcs,
        args = args,
        **kwargs
    )

def lint_all():
    py_srcs = native.glob(["*.py"])
    if py_srcs:
        pycodestyle_test(name = "pycodestyle_test", srcs = py_srcs)
    bzl_srcs = native.glob(["WORKSPACE", "WORKSPACE.bazel", "BUILD", "BUILD.bazel", "*.bzl"])
    if bzl_srcs:
        buildifier_test(name = "buildifier_test", srcs = bzl_srcs)
