import os
import sys

from bazel_tools.tools.python.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/interactive_judge/server.data')
    assert location and os.path.exists(location), location

    with open(sys.argv[1]) as f:
        a, b = map(int, f.read().split())

    print('PEER: init: a=%d, b=%d' % (a, b), file=sys.stderr)

    while True:
        line = input()
        print('PEER: input: %s' % line, file=sys.stderr)
        if line.startswith('q '):
            x = int(line.split()[1])
            print('PEER: output: %d' % (a * x + b), file=sys.stderr)
            print(a * x + b)
            sys.stdout.flush()
        elif line.startswith('a '):
            p, q = map(int, line.split()[1:])
            assert (p, q) == (a, b)
            break


if __name__ == '__main__':
    main()
