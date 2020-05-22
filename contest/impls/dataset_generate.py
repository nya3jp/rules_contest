import argparse
import os
import subprocess
import tempfile

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    options = parser.parse_args()

    with tempfile.TemporaryDirectory() as dataset_dir:
        env = os.environ.copy()
        env['OUTPUT_DIR'] = dataset_dir
        subprocess.check_call(
            [options.executable],
            env=env)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
