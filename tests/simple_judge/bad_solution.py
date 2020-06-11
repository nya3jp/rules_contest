import os

from bazel_tools.tools.python.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/simple_judge/data.txt')
    assert location and os.path.exists(location), location

    print(int(input()) * 28)


if __name__ == '__main__':
    main()
