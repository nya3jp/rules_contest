# Creating a New Workspace

This section describes how to create a new workspace maintaining programming
contest problems using `rules_contest`.

## What is a workspace?

A workspace is a concept of [Bazel]. A workspace is a directory on your
filesystem that contains the source files needed to build and test programs.
A workspace directory has a text file named `WORKSPACE` which might be empty or
contain some workspace configurations.

[Bazel]: https://bazel.build/

## Creating a workspace using the template (recommended)

We provide [a Git repository] containing a template workspace on GitHub.
Click the "[Use this template]" button to create a new repository using
the template. Use [Git] to checkout the repository to the local machine.

[a Git repository]: https://github.com/nya3jp/contest_template
[Use this template]: https://help.github.com/articles/creating-a-repository-from-a-template/
[Git]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

## Standard workspace layout

Since Bazel rules provided by `rules_contest` make no assumption about file
locations, you can organize your workspace files in any way you like.
That said, if your workspace is for maintaining problems for a programming
contest event, it is recommended to place workspace files in the following
*standard workspace layout*. The template workspace has this layout.

- Workspace root directory
    - Problem 1 directory
        - Judge directory
        - Solution A directory
        - Solution B directory
        - ...
    - Problem 2 directory
        - Judge directory
        - Solution A directory
        - Solution B directory
    - ...

## Settings

### WORKSPACE

`WORKSPACE` file in the workspace directory should include the following
external dependency to use `rules_contest`.

```python
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "rules_contest",
    remote = "https://github.com/nya3jp/rules_contest",
    branch = "v0.5.7",
)
```

### .gitignore (optional)

Bazel creates symbolic links named `bazel-*` in the workspace directory.
It is recommended to add them to the `.gitignore` file so that you and your
collaborators do not accidentally commit those them.

```
/bazel-*
```

### .bazelrc (optional)

You can place `.bazelrc` file in the workspace directory to override Bazel's
default configurations. Some configurations are recommended.

```text
# Enable optimization by default.
# Without this setting, C++ programs are much slower.
build -c opt

# Disable test coverage reporting by default.
# Without this setting, running any test requires downloading JDK, even if
# no Java program is in the workspace.
build --coverage_report_generator=@rules_contest//contest:fake_coverage_report_generator
```

### prelude_bazel (optional)

`tools/build_rules/prelude_bazel` file is read by Bazel before evaluating any
`BUILD` file. You can load rules provided by `rules_contest` to avoid explicitly
loading them in each `BUILD` file.

```python
load("@rules_contest//contest:defs.bzl",
    "dataset_generate",
    "dataset_derive",
    "dataset_merge",
    "dataset_test",
    "simple_judge",
    "solution_test",
    "sample_test",
    "jinja2_template",
    "markdown",
    "cc_yaml_library",
    "py_yaml_library")
```

## Configuring continuous integration

It is likely that you want to set up a continuous integration to build and test
your workspace periodically or on every commit. See [the template repository]
for an example configuration of GitHub Actions.

[the template repository]: https://github.com/nya3jp/contest_template/tree/master/.github/workflows
