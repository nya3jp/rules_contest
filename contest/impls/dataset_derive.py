import argparse
import os
import subprocess

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
        for name in datasets.names(dataset_dir):
            input_path = os.path.join(dataset_dir, name + '.' + options.input_extension)
            if not os.path.exists(input_path):
                continue
            output_path = os.path.join(dataset_dir, name + '.' + options.output_extension)
            if os.path.exists(output_path):
                continue
            with open(input_path, 'rb') as input_file:
                with open(output_path, 'wb') as output_file:
                    subprocess.check_call(
                        [options.executable],
                        stdin=input_file,
                        stdout=output_file)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
