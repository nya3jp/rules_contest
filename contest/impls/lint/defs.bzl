def pycodestyle_test(name, srcs, **kwargs):
    native.py_test(
        name = name,
        srcs = ["//third_party/pycodestyle:pycodestyle.py"] + srcs,
        main = "//third_party/pycodestyle:pycodestyle.py",
        args = ["$(rootpath " + src + ")" for src in srcs],
        **kwargs
    )
