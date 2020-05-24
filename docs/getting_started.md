# Getting Started

This section tells you how to create a new workspace for managing
programming contest problems.

## Prerequisites

[Bazel] is required to use `rules_contest`. Install it by following
[the official guide].

[Bazel]: https://bazel.build/
[the official guide]: https://docs.bazel.build/versions/master/install.html

## Clone the template repository

We provide [a Git repository] containing a template workspace on GitHub.
Click the "[Use this template]" button to create a new repository using
the template. Use [Git] to checkout the repository to the local machine.

[a Git repository]: https://github.com/nya3jp/contest_template
[Use this template]: https://help.github.com/articles/creating-a-repository-from-a-template/
[Git]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

The template workspace contains two mock problems ("Sum of two numbers" and
"Square root"), as well as several reference solutions to them.

## Build all targets

In the workspace, run the following command to build all datasets and reference
solutions.

```console
bazel build //...
```

Build artifacts are saved under the `bazel-bin` directory in the workspace.
For example, the dataset for the "Sum of two numbers" problem is at
`bazel-bin/sum/judge/dataset.zip`.

## Test all targets

In the workspace, run the following command to test all datasets and reference
solutions.

```console
bazel test //...
```

In the end of the output, a summary of test results is printed to the console.

```console
//sqrt/judge:dataset_test                                                PASSED in 1.2s
//sqrt/judge:sample_test                                                 PASSED in 0.5s
//sqrt/python:python_test                                                PASSED in 2.8s
//sum/cpp:cpp_test                                                       PASSED in 0.7s
//sum/cpp_WA:cpp_WA_test                                                 PASSED in 0.7s
//sum/judge:dataset_test                                                 PASSED in 1.3s
//sum/judge:sample_test                                                  PASSED in 0.4s
//sum/python:python_test                                                 PASSED in 1.7s
```
