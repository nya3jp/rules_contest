import argparse
import os
import subprocess
import tempfile

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--command', required=True)
    options = parser.parse_args()

    with tempfile.TemporaryDirectory() as dataset_dir:
        env = os.environ.copy()
        env.update({
            'EXEC': options.executable,
            'OUTPUT_DIR': dataset_dir,
        })
        subprocess.check_call(
            ["bash", "-e", "-c", options.command],
            env=env)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
