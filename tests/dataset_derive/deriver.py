import argparse
import os

from bazel_tools.tools.python.runfiles import runfiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--multiplier', type=int, default=11)
    options = parser.parse_args()

    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/dataset_derive/data.txt')
    assert location and os.path.exists(location), location

    value = int(input())
    print(value * options.multiplier)


if __name__ == '__main__':
    main()
