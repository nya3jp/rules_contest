import os
import sys

from bazel_tools.tools.python.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/interactive_judge/solution.data')
    assert location and os.path.exists(location), location

    print('SOLUTION: output: a 0 0', file=sys.stderr)
    print('a 0 0')


if __name__ == '__main__':
    main()
