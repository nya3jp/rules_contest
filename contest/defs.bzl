def dataset_generate(name, exec, **kwargs):
    """Generates a new dataset by running an executable.

    The executable should write generated data files to $OUTPUT_DIR.

    Args:
      name: A unique name for this rule.
      exec: The label of an executable.
    """
    out = name + ".zip"
    args = [
        "'$(execpath @rules_contest//contest/impls:dataset_generate)'",
        "--output='$@'",
        "--executable='$(execpath " + exec + ")'",
    ]
    native.genrule(
        name = name,
        outs = [out],
        tools = ["@rules_contest//contest/impls:dataset_generate", exec],
        cmd = " ".join(args),
        **kwargs
    )

def dataset_derive(name, exec, dataset, input_extension = "in", output_extension = "ans", **kwargs):
    out = name + ".zip"
    args = [
        "'$(execpath @rules_contest//contest/impls:dataset_derive)'",
        "--output='$@'",
        "--executable='$(execpath " + exec + ")'",
        "--dataset='$<'",
        "--input_extension='" + input_extension + "'",
        "--output_extension='" + output_extension + "'",
    ]
    native.genrule(
        name = name,
        outs = [out],
        srcs = [dataset],
        tools = ["@rules_contest//contest/impls:dataset_derive", exec],
        cmd = " ".join(args),
        **kwargs
    )

def dataset_merge(name, files = [], datasets = [], **kwargs):
    out = name + ".zip"
    args = [
        "'$(execpath @rules_contest//contest/impls:dataset_merge)'",
        "--output='$@'",
    ]
    for file in files:
        args.append("--file='$(execpath %s)'" % file)
    for dataset in datasets:
        args.append("--dataset='$(execpath %s)'" % dataset)
    native.genrule(
        name = name,
        outs = [out],
        srcs = files + datasets,
        tools = ["@rules_contest//contest/impls:dataset_merge"],
        cmd = " ".join(args),
        **kwargs
    )

def dataset_test(name, exec, dataset, input_extension = "in", **kwargs):
    sh = name + ".sh"
    args = [
        "'$(execpath @rules_contest//contest/impls:dataset_test_wrapper_generator)'",
        "--output='$@'",
        "--dataset_test='$(rootpath @rules_contest//contest/impls:dataset_test)'",
        "--executable='$(rootpath " + exec + ")'",
        "--dataset='$(rootpath " + dataset + ")'",
        "--input_extension='" + input_extension + "'",
    ]
    native.genrule(
        name = name + "_sh",
        outs = [sh],
        srcs = [dataset],
        tools = [
            "@rules_contest//contest/impls:dataset_test_wrapper_generator",
            "@rules_contest//contest/impls:dataset_test",
            exec,
        ],
        executable = True,
        cmd = " ".join(args),
    )
    native.sh_test(
        name = name,
        srcs = [sh],
        data = ["@rules_contest//contest/impls:dataset_test", exec, dataset],
        **kwargs
    )

def simple_judge(name, dataset, comparator = "@rules_contest//contest:exact_comparator", input_extension = "in", answer_extension = "ans", _metadata = {}, **kwargs):
    full_name = "//" + native.package_name() + ":" + name
    if native.repository_name() != "@":
        full_name = native.repository_name() + full_name
    sh = name + ".sh"
    args = [
        "'$(execpath @rules_contest//contest/impls:simple_judge_wrapper_generator)'",
        "--output='$@'",
        "--judge_name=" + full_name,
        "--simple_judge='$(rootpath @rules_contest//contest/impls:simple_judge)'",
        "--comparator='$(rootpath " + comparator + ")'",
        "--dataset='$(rootpath " + dataset + ")'",
        "--input_extension='" + input_extension + "'",
        "--answer_extension='" + answer_extension + "'",
    ]
    args.extend([
        "--metadata=%s:%s" % (key, value)
        for key, value in sorted(_metadata.items())
    ])
    native.genrule(
        name = name + "_gen",
        outs = [sh],
        srcs = [dataset],
        tools = [
            "@rules_contest//contest/impls:simple_judge_wrapper_generator",
            "@rules_contest//contest/impls:simple_judge",
            comparator,
        ],
        executable = True,
        cmd = " ".join(args),
    )
    native.sh_binary(
        name = name,
        srcs = [sh],
        data = ["@rules_contest//contest/impls:simple_judge", comparator, dataset],
        **kwargs
    )

def solution_test(name, solution, judge, judge_args = [], exclusive = True, **kwargs):
    sh = name + ".sh"
    args = [
        "'$(execpath @rules_contest//contest/impls:solution_test_wrapper_generator)'",
        "--output='$@'",
        "--judge='$(rootpath " + judge + ")'",
        "--solution='$(rootpath " + solution + ")'",
        "--",
    ] + judge_args
    native.genrule(
        name = name + "_gen",
        outs = [sh],
        tools = ["@rules_contest//contest/impls:solution_test_wrapper_generator", solution, judge],
        executable = True,
        cmd = " ".join(args),
    )
    tags = kwargs.setdefault("tags", [])
    tags.append("solution")
    if exclusive:
        tags.append("exclusive")
    native.sh_test(
        name = name,
        srcs = [sh],
        data = [solution, judge],
        **kwargs
    )

def sample_test(name, files, judge, judge_args = [], output_extension = "out", **kwargs):
    sh = name + "_solution.sh"
    args = [
        "'$(execpath @rules_contest//contest/impls:sample_test_solution_generator)'",
        "--output='$@'",
        "--output_extension='" + output_extension + "'",
    ]
    for file in files:
        args.append("$(rootpaths %s)" % file)
    native.genrule(
        name = name + "_solution_gen",
        outs = [sh],
        srcs = files,
        tools = ["@rules_contest//contest/impls:sample_test_solution_generator"],
        executable = True,
        cmd = " ".join(args),
    )
    bin_name = name + "_solution"
    native.sh_binary(
        name = bin_name,
        srcs = [sh],
        data = files,
    )
    solution_test(
        name = name,
        solution = ":" + bin_name,
        judge = judge,
        judge_args = judge_args,
        **kwargs
    )

def jinja2_template(name, srcs, main = None, files = [], vars = [], dataset = None, **kwargs):
    if len(srcs) == 1:
        main = srcs[0]
    if not main:
        fail("main must be specified for multi-file templates")
    if main not in srcs:
        fail("main must be one of srcs")
    args = [
        "'$(execpath @rules_contest//contest/impls:jinja2_template)'",
        "--output='$@'",
        "--input='$(execpath " + main + ")'",
    ]
    if dataset:
        args.append("--dataset='$(execpath " + dataset + ")'")
    for file in files:
        args.append("--file='$(execpaths %s)'" % file)
    for file in vars:
        args.append("--vars='$(execpaths %s)'" % file)
    deps = srcs + files + vars
    if dataset:
        deps.append(dataset)
    out = name + ".rendered"
    native.genrule(
        name = name,
        outs = [out],
        srcs = deps,
        tools = ["@rules_contest//contest/impls:jinja2_template"],
        cmd = " ".join(args),
        **kwargs
    )

def markdown(name, src, **kwargs):
    html = name + ".html"
    native.genrule(
        name = name,
        outs = [html],
        srcs = [src],
        tools = ["@rules_contest//contest/impls:render_markdown"],
        cmd = "'$(execpath @rules_contest//contest/impls:render_markdown)' \
            --output='$@' \
            --input='$<' \
            ",
        **kwargs
    )

def cc_yaml_library(name, src, **kwargs):
    gen_name = name + "_gen"
    out = src.rsplit(".", 2)[0] + ".h"
    native.genrule(
        name = gen_name,
        outs = [out],
        srcs = [src],
        tools = ["@rules_contest//contest/impls:cc_yaml_library"],
        cmd = "'$(execpath @rules_contest//contest/impls:cc_yaml_library)' \
            --output='$@' \
            --input='$<' \
            ",
        **kwargs
    )
    native.cc_library(
        name = name,
        hdrs = [out],
        **kwargs
    )

def py_yaml_library(name, src, **kwargs):
    gen_name = name + "_gen"
    out = src.rsplit(".", 2)[0] + ".py"
    native.genrule(
        name = gen_name,
        outs = [out],
        srcs = [src],
        tools = ["@rules_contest//contest/impls:py_yaml_library"],
        cmd = "'$(execpath @rules_contest//contest/impls:py_yaml_library)' \
            --output='$@' \
            --input='$<' \
            ",
        **kwargs
    )
    native.py_library(
        name = name,
        srcs = [out],
        srcs_version = "PY2AND3",
        **kwargs
    )
