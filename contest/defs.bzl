def dataset_generate(name, exec, **kwargs):
    out = name + ".zip"
    native.genrule(
        name = name,
        outs = [out],
        tools = ["@rules_contest//contest/impls:dataset_generate", exec],
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_generate)' \
            --output='$@' \
            --executable='$(execpath " + exec + ")'",
        **kwargs
    )


def dataset_derive(name, exec, datasets, input_extension="in", output_extension="diff", **kwargs):
    out = name + ".zip"
    native.genrule(
        name = name,
        outs = [out],
        srcs = datasets,
        tools = ["@rules_contest//contest/impls:dataset_derive", exec],
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_derive)' \
            --output='$@' \
            --input_extension='" + input_extension + "' \
            --output_extension='" + output_extension + "' \
            --executable='$(execpath " + exec + ")' \
            $(SRCS)",
        **kwargs
    )


def dataset_merge(name, datasets, **kwargs):
    out = name + ".zip"
    native.genrule(
        name = name,
        outs = [out],
        srcs = datasets,
        tools = ["@rules_contest//contest/impls:dataset_merge"],
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_merge)' \
            --output='$@' \
            $(SRCS)",
        **kwargs
    )


def dataset_test(name, exec, datasets, input_extension="in", **kwargs):
    zip = name + "_dataset.zip"
    native.genrule(
        name = name + "_dataset_zip",
        outs = [zip],
        srcs = datasets,
        tools = ["@rules_contest//contest/impls:dataset_merge"],
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_merge)' \
            --output='$@' \
            $(SRCS)",
    )
    sh = name + ".sh"
    native.genrule(
        name = name + "_sh",
        outs = [sh],
        srcs = [zip],
        tools = [
            "@rules_contest//contest/impls:dataset_test_wrapper_generator",
            "@rules_contest//contest/impls:dataset_test",
            exec,
        ],
        executable = True,
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_test_wrapper_generator)' \
            --output='$@' \
            --dataset_test='$(rootpath @rules_contest//contest/impls:dataset_test)' \
            --executable='$(rootpath " + exec + ")' \
            --input_extension='" + input_extension + "' \
            $(rootpath " + zip + ")",
    )
    native.sh_test(
        name = name,
        srcs = [sh],
        data = [
            "@rules_contest//contest/impls:dataset_test",
            exec,
            zip,
        ],
        **kwargs
    )


def simple_judge(name, datasets, comparator="@rules_contest//contest:exact_comparator", input_extension="in", answer_extension="diff", **kwargs):
    zip = name + "_dataset.zip"
    native.genrule(
        name = name + "_dataset_zip",
        outs = [zip],
        srcs = datasets,
        tools = ["@rules_contest//contest/impls:dataset_merge"],
        cmd = "'$(execpath @rules_contest//contest/impls:dataset_merge)' \
            --output='$@' \
            $(SRCS)",
    )
    sh = name + ".sh"
    native.genrule(
        name = name + "_sh",
        outs = [sh],
        srcs = [zip],
        tools = ["@rules_contest//contest/impls:simple_judge_wrapper_generator", "@rules_contest//contest/impls:simple_judge", comparator],
        executable = True,
        cmd = "'$(execpath @rules_contest//contest/impls:simple_judge_wrapper_generator)' \
            --output='$@' \
            --judge='$(rootpath @rules_contest//contest/impls:simple_judge)' \
            --comparator='$(rootpath " + comparator + ")' \
            --dataset='$(rootpath " + zip + ")' \
            --input_extension='" + input_extension + "' \
            --answer_extension='" + answer_extension + "' \
            ",
    )
    native.sh_binary(
        name = name,
        srcs = [sh],
        data = ["@rules_contest//contest/impls:simple_judge", comparator, zip],
        **kwargs
    )


def solution_test(name, solution, judge, judge_args=[], **kwargs):
    sh = name + ".sh"
    native.genrule(
        name = name + "_sh",
        outs = [sh],
        tools = ["@rules_contest//contest/impls:solution_test_wrapper_generator", solution, judge],
        executable = True,
        cmd = "'$(execpath @rules_contest//contest/impls:solution_test_wrapper_generator)' \
            --output='$@' \
            --judge='$(rootpath " + judge + ")' \
            --solution='$(rootpath " + solution + ")' \
            -- \
            " + " ".join(judge_args),
    )
    native.sh_test(
        name = name,
        srcs = [sh],
        data = [solution, judge],
        **kwargs
    )
