import os
import sys

from third_party.runfiles import runfiles


def main():
    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/dataset_test/validator.data')
    assert location and os.path.exists(location), location

    if len(sys.argv) < 2:
        n = int(input())
    else:
        with open(sys.argv[1]) as f:
            n = int(f.read().strip())

    assert n % 2 == 0


if __name__ == '__main__':
    main()
