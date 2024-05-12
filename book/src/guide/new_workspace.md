# Creating a New Workspace

This section describes how to create a new workspace maintaining programming
contest problems using `rules_contest`.

## What is a workspace?

A workspace is a concept of [Bazel]. A workspace refers to a set of
*repositories*, namely the main repository which is the primary directory
tree where you maintain source code for your project, and external
repositories that are imported directly or indirectly by the main repository.
The root directory of a repository contains a text file named
`MODULE.bazel` (or alternatively, `REPO.bazel`, `WORKSPACE.bazel`,
`WORKSPACE`) to declare that it's a Bazel repository.

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

### MODULE.bazel

`MODULE.bazel` file in the workspace directory should include the following
external dependency to use `rules_contest`.

```python
bazel_dep(name = "rules_contest", version = "0.9.0")
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
```

## Configuring continuous integration

It is likely that you want to set up a continuous integration to build and test
your workspace periodically or on every commit. See [the template repository]
for an example configuration of GitHub Actions.

[the template repository]: https://github.com/nya3jp/contest_template/tree/master/.github/workflows
