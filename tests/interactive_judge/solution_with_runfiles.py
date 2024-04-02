import os
import sys

from third_party.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/interactive_judge/solution.data')
    assert location and os.path.exists(location), location

    print('SOLUTION: output: q 0', file=sys.stderr)
    print('q 0')
    sys.stdout.flush()
    b = int(input())
    print('SOLUTION: input: %d' % b, file=sys.stderr)

    print('SOLUTION: output: q 1', file=sys.stderr)
    print('q 1')
    sys.stdout.flush()
    ab = int(input())
    print('SOLUTION: input: %d' % ab, file=sys.stderr)

    a = ab - b

    print('SOLUTION: output: a %d %d' % (a, b), file=sys.stderr)
    print('a %d %d' % (a, b))


if __name__ == '__main__':
    main()
