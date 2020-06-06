import argparse
import os
import shutil
import tempfile

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--file', dest='files', action='append', default=[])
    parser.add_argument('--dataset', dest='datasets', action='append', default=[])
    options = parser.parse_args()

    with tempfile.TemporaryDirectory() as dataset_dir:
        for path in options.files:
            shutil.copy(path, os.path.join(dataset_dir, os.path.basename(path)))
        for path in options.datasets:
            datasets.extract(path, dataset_dir)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
