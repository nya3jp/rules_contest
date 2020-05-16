import argparse
import os
import subprocess

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('datasets', nargs='*')
    options = parser.parse_args()

    with datasets.expand(options.datasets) as dataset_dir:
        subprocess.check_call(
            ['zip', '-q', '-r', os.path.abspath(options.output), '.'],
            cwd=dataset_dir)


if __name__ == '__main__':
    main()
