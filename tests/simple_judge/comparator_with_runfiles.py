import argparse
import os

from bazel_tools.tools.python.runfiles import runfiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    parser.add_argument('answer_file')
    options = parser.parse_args()

    # Make sure we have access to the data file.
    resolver = runfiles.Create()
    location = resolver.Rlocation('rules_contest/tests/simple_judge/comparator.data')
    assert location and os.path.exists(location), location

    with open(options.input_file) as f:
        input_num = int(f.read().strip())
    with open(options.output_file) as f:
        output_num = int(f.read().strip())

    assert output_num == input_num * 42


if __name__ == '__main__':
    main()
