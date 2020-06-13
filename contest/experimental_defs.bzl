def domjudge_package(name, dataset, domjudge_metadata = None, icpc_metadata = None, statements = [], **kwargs):
    out = name + ".zip"
    args = [
        "'$(execpath @rules_contest//contest/impls:domjudge_package)'",
        "--output='$@'",
        "--dataset='$(execpath " + dataset + ")'",
    ]
    srcs = [dataset]
    if domjudge_metadata:
        args.append("--domjudge_metadata='$(execpath " + domjudge_metadata + ")'")
        srcs.append(domjudge_metadata)
    if icpc_metadata:
        args.append("--icpc_metadata='$(execpath " + icpc_metadata + ")'")
        srcs.append(icpc_metadata)
    for statement in statements:
        args.append("--statement='$(execpath " + statement + ")'")
        srcs.append(statement)
    native.genrule(
        name = name,
        outs = [out],
        srcs = srcs,
        tools = ["@rules_contest//contest/impls:domjudge_package"],
        cmd = " ".join(args),
        **kwargs
    )
