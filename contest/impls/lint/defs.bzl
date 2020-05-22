def pycodestyle_test(name, srcs, **kwargs):
    args = ["--max-line-length=160"]
    args.extend(["$(rootpath " + src + ")" for src in srcs])
    native.py_test(
        name = name,
        srcs = ["//third_party/pycodestyle:pycodestyle.py"] + srcs,
        main = "//third_party/pycodestyle:pycodestyle.py",
        args = args,
        **kwargs
    )
