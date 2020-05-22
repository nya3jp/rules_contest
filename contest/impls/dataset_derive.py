import argparse
import os
import subprocess
import sys

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('--output_extension', required=True)
    options = parser.parse_args()

    with datasets.expand(options.dataset) as dataset_dir:
        for case in datasets.cases(dataset_dir):
            input_path = case.files.get(options.input_extension)
            if not input_path:
                sys.exit('%s.%s not found' % (case.name, options.input_extension))
            if options.output_extension in case.files:
                continue
            output_path = os.path.join(dataset_dir, case.name + '.' + options.output_extension)
            with open(input_path, 'rb') as input_file:
                with open(output_path, 'wb') as output_file:
                    subprocess.check_call(
                        [options.executable],
                        stdin=input_file,
                        stdout=output_file)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
