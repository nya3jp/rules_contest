import os

from bazel_tools.tools.python.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/simple_judge/solution.data')
    assert location and os.path.exists(location), location

    n = int(input())
    if n == 1:
        print(42)
    else:
        print(28)


if __name__ == '__main__':
    main()
