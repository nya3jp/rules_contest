# rules_contest

[![test](https://github.com/nya3jp/rules_contest/workflows/test/badge.svg)][test]
[![docs](https://readthedocs.org/projects/rules-contest/badge/?version=latest&style=flat)][docs]
[![license](https://img.shields.io/github/license/nya3jp/rules_contest)][license]
[![releases](https://img.shields.io/github/v/tag/nya3jp/rules_contest)][releases]

`rules_contest` is a collection of [Bazel] rules for maintaining programming
contest problems. `rules_contest` helps you automate tasks to prepare
programming contest problems, such as:

- Building and testing datasets
- Building and testing reference solutions
- Building problem statements
- Building a progress tracker

Rules provided by `rules_contest` are designed to be simple and composable.
Even if some existing rules do not fit your purpose, you can easily replace
them with your own custom rules while still using other useful rules.

[test]: https://github.com/nya3jp/rules_contest/actions?query=workflow%3Atest
[docs]: https://rules-contest.readthedocs.io/
[license]: https://github.com/nya3jp/rules_contest/blob/master/LICENSE
[releases]: https://github.com/nya3jp/rules_contest/releases/
[Bazel]: https://bazel.build/

## Getting Started

### Prerequisites

Install [Bazel] by following [the official guide].

[Bazel]: https://bazel.build/
[the official guide]: https://docs.bazel.build/versions/master/install.html

### Clone the template repository

We provide a Git repository containing a template workspace on GitHub.

[![https://github.com/nya3jp/contest_template](https://img.shields.io/badge/repo-nya3jp%2Fcontest__template-blue?logo=github)][contest_template]

Click the "[Use this template]" button to create a new repository using
the template. Use [Git] to checkout the repository to the local machine.

[contest_template]: https://github.com/nya3jp/contest_template
[Use this template]: https://help.github.com/articles/creating-a-repository-from-a-template/
[Git]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

The template workspace contains a few example problems and their solutions.

### Build all targets

In the workspace, run the following command to build all datasets and solutions.

```console
bazel build //...
```

Build artifacts are saved under the `bazel-bin` directory in the workspace.
For example, the dataset for the "Sum of two numbers" problem is at
`bazel-bin/sum/judge/dataset.zip`.

### Test all targets

In the workspace, run the following command to test all datasets and solutions.

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

## Documentation

Full documentation is available online.

[![docs](https://readthedocs.org/projects/rules-contest/badge/?version=latest&style=flat)][docs]

[docs]: https://rules-contest.readthedocs.io/
