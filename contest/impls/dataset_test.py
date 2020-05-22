import argparse
import os
import subprocess
import sys

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    options = parser.parse_args()

    with datasets.expand(options.dataset) as dataset_dir:
        for case in datasets.cases(dataset_dir):
            input_path = case.files.get(options.input_extension)
            if not input_path:
                sys.exit('%s.%s not found' % (case.name, options.input_extension))

            print('======= %s' % case.name)
            with open(input_path, 'rb') as input_file:
                env = os.environ.copy()
                env.update(case.env)
                subprocess.check_call([options.executable], stdin=input_file, env=env)


if __name__ == '__main__':
    main()
