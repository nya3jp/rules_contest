workspace(name = "rules_contest")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_file")

git_repository(
    name = "io_bazel_stardoc",
    remote = "https://github.com/bazelbuild/stardoc.git",
    tag = "0.4.0",
)

load("@io_bazel_stardoc//:setup.bzl", "stardoc_repositories")

stardoc_repositories()

http_file(
    name = "buildifier_prebuilt_linux",
    sha256 = "e92a6793c7134c5431c58fbc34700664f101e5c9b1c1fcd93b97978e8b7f88db",
    urls = ["https://github.com/bazelbuild/buildtools/releases/download/3.0.0/buildifier"],
)

http_file(
    name = "buildifier_prebuilt_mac",
    sha256 = "acfa34087ae386b1c02c224ca685dc132e53790d0b95f7649c728e46f4b53870",
    urls = ["https://github.com/bazelbuild/buildtools/releases/download/3.0.0/buildifier.mac"],
)

http_file(
    name = "buildifier_prebuilt_windows",
    sha256 = "5134ada7526882398b4bf014efefe18aa0c59253cbbd6525a9e002ba11300f34",
    urls = ["https://github.com/bazelbuild/buildtools/releases/download/3.0.0/buildifier.exe"],
)
