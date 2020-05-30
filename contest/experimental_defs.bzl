def domjudge_package(name, metadata, dataset, statements = [], **kwargs):
    out = name + ".zip"
    args = [
        "'$(execpath @rules_contest//contest/impls:domjudge_package)'",
        "--output='$@'",
        "--metadata='$(execpath " + metadata + ")'",
        "--dataset='$(execpath " + dataset + ")'",
    ]
    for statement in statements:
        args.append("--statement='$(execpath " + statement + ")'")
    native.genrule(
        name = name,
        outs = [out],
        srcs = [metadata, dataset] + statements,
        tools = ["@rules_contest//contest/impls:domjudge_package"],
        cmd = " ".join(args),
        **kwargs
    )
