def _dataset_generate_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name + ".zip")
    ctx.actions.run(
        outputs = [out],
        executable = ctx.executable._tool,
        tools = [ctx.executable.exec],
        arguments = [
            "--output=" + out.path,
            "--executable=" + ctx.executable.exec.path,
            "--command=" + ctx.attr.cmd,
        ],
        mnemonic = "DatasetGenerate",
        progress_message = "Generating " + out.basename,
    )
    return [
        # TODO: Figure out why runfiles is needed even though this is not an
        # executable rule. Without it, a generated zip file is not included
        # to runfiles of binaries.
        DefaultInfo(files = depset([out]), runfiles = ctx.runfiles([out])),
    ]

dataset_generate = rule(
    implementation = _dataset_generate_impl,
    attrs = {
        "exec": attr.label(
            mandatory = True,
            executable = True,
            cfg = "host",
        ),
        "cmd": attr.string(
            default = "${EXEC}",
        ),
        "_tool": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:dataset_generate"),
        ),
    },
)

def _dataset_derive_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name + ".zip")
    ctx.actions.run(
        outputs = [out],
        inputs = [ctx.file.dataset],
        executable = ctx.executable._tool,
        tools = [ctx.executable.exec],
        arguments = [
            "--output=" + out.path,
            "--executable=" + ctx.executable.exec.path,
            "--dataset=" + ctx.file.dataset.path,
            "--command=" + ctx.attr.cmd,
        ],
        mnemonic = "DatasetGenerate",
        progress_message = "Generating " + out.basename,
    )
    return [
        # TODO: Figure out why runfiles is needed even though this is not an
        # executable rule. Without it, a generated zip file is not included
        # to runfiles of binaries.
        DefaultInfo(files = depset([out]), runfiles = ctx.runfiles([out])),
    ]

dataset_derive = rule(
    implementation = _dataset_derive_impl,
    attrs = {
        "exec": attr.label(
            mandatory = True,
            executable = True,
            cfg = "host",
        ),
        "dataset": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "cmd": attr.string(
            default = "${EXEC} < ${INPUT_DIR}/${TESTCASE}.in > ${OUTPUT_DIR}/${TESTCASE}.ans",
        ),
        "_tool": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:dataset_derive"),
        ),
    },
)

def _dataset_merge_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name + ".zip")
    args = ["--output=" + out.path]
    for f in ctx.files.files:
        args.append("--file=" + f.path)
    for f in ctx.files.datasets:
        args.append("--dataset=" + f.path)
    ctx.actions.run(
        outputs = [out],
        inputs = ctx.files.files + ctx.files.datasets,
        executable = ctx.executable._tool,
        arguments = args,
        mnemonic = "DatasetMerge",
        progress_message = "Generating " + out.basename,
    )
    return [
        # TODO: Figure out why runfiles is needed even though this is not an
        # executable rule. Without it, a generated zip file is not included
        # to runfiles of binaries.
        DefaultInfo(files = depset([out]), runfiles = ctx.runfiles([out])),
    ]

dataset_merge = rule(
    implementation = _dataset_merge_impl,
    attrs = {
        "files": attr.label_list(
            allow_files = True,
        ),
        "datasets": attr.label_list(
            allow_files = True,
        ),
        "_tool": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:dataset_merge"),
        ),
    },
)

def _dataset_test_impl(ctx):
    out = ctx.outputs.executable
    ctx.actions.run(
        outputs = [out],
        executable = ctx.executable._generator,
        arguments = [
            "--output=" + out.path,
            "--dataset_test=" + ctx.executable._dataset_test.short_path,
            "--executable=" + ctx.executable.exec.short_path,
            "--dataset=" + ctx.file.dataset.short_path,
            "--command=" + ctx.attr.cmd,
        ],
        mnemonic = "DatasetTest",
        progress_message = "Generating " + out.basename,
    )
    runfiles = ctx.attr._dataset_test[DefaultInfo].default_runfiles
    runfiles = runfiles.merge(ctx.attr.exec[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge(ctx.runfiles(ctx.files.dataset))
    return [DefaultInfo(runfiles = runfiles)]

dataset_test = rule(
    implementation = _dataset_test_impl,
    attrs = {
        "exec": attr.label(
            mandatory = True,
            executable = True,
            cfg = "host",
        ),
        "dataset": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "cmd": attr.string(
            default = "${EXEC} < ${INPUT_DIR}/${TESTCASE}.in",
        ),
        "_dataset_test": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:dataset_test"),
        ),
        "_generator": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:dataset_test_wrapper_generator"),
        ),
    },
    test = True,
)

def _simple_judge_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.run(
        outputs = [out],
        executable = ctx.executable._generator,
        arguments = [
            "--output=" + out.path,
            "--judge_name=" + str(ctx.label),
            "--simple_judge=" + ctx.executable._simple_judge.short_path,
            "--comparator=" + ctx.executable.comparator.short_path,
            "--dataset=" + ctx.file.dataset.short_path,
            "--solution_command=" + ctx.attr.solution_cmd,
            "--comparator_command=" + ctx.attr.comparator_cmd,
            "--case_timeout=%d" % ctx.attr.case_timeout,
        ],
        mnemonic = "SimpleJudge",
        progress_message = "Generating " + out.basename,
    )
    runfiles = ctx.runfiles([out])
    runfiles = runfiles.merge(ctx.attr._simple_judge[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge(ctx.attr.comparator[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge(ctx.runfiles(ctx.files.dataset))
    return [DefaultInfo(files = depset([out]), runfiles = runfiles)]

simple_judge = rule(
    implementation = _simple_judge_impl,
    attrs = {
        "dataset": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "comparator": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest:exact_comparator"),
        ),
        "solution_cmd": attr.string(
            default = "${EXEC} < ${INPUT_DIR}/${TESTCASE}.in > ${OUTPUT_FILE}",
        ),
        "comparator_cmd": attr.string(
            default = "${EXEC} ${INPUT_DIR}/${TESTCASE}.in ${OUTPUT_FILE} ${INPUT_DIR}/${TESTCASE}.ans",
        ),
        "case_timeout": attr.int(
            default = 10,
        ),
        "_simple_judge": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:simple_judge"),
        ),
        "_generator": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:simple_judge_wrapper_generator"),
        ),
    },
)

def _interactive_judge_impl(ctx):
    out = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.run(
        outputs = [out],
        executable = ctx.executable._generator,
        arguments = [
            "--output=" + out.path,
            "--judge_name=" + str(ctx.label),
            "--interactive_judge=" + ctx.executable._interactive_judge.short_path,
            "--exec=" + ctx.executable.exec.short_path,
            "--dataset=" + ctx.file.dataset.short_path,
            "--command=" + ctx.attr.cmd,
            "--case_timeout=%d" % ctx.attr.case_timeout,
        ],
        mnemonic = "InteractiveJudge",
        progress_message = "Generating " + out.basename,
    )
    runfiles = ctx.runfiles([out])
    runfiles = runfiles.merge(ctx.attr._interactive_judge[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge(ctx.attr.exec[DefaultInfo].default_runfiles)
    runfiles = runfiles.merge(ctx.runfiles(ctx.files.dataset))
    return [DefaultInfo(files = depset([out]), runfiles = runfiles)]

interactive_judge = rule(
    implementation = _interactive_judge_impl,
    attrs = {
        "dataset": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "exec": attr.label(
            mandatory = True,
            executable = True,
            cfg = "host",
        ),
        "cmd": attr.string(
            default = "${EXEC} ${INPUT_DIR}/${TESTCASE}.in",
        ),
        "case_timeout": attr.int(
            default = 10,
        ),
        "_interactive_judge": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:interactive_judge"),
        ),
        "_generator": attr.label(
            executable = True,
            cfg = "host",
            default = Label("//contest/impls:interactive_judge_wrapper_generator"),
        ),
    },
)

def solution_test(name, solution, judge, judge_args = [], tags = [], **kwargs):
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
    native.sh_test(
        name = name,
        srcs = [sh],
        data = [solution, judge],
        tags = tags + ["solution"],
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
