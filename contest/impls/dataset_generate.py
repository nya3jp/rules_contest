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
        # Remove RUNFILES_ variables so as not to confuse the executable.
        env = {
            key: value
            for key, value in env.items()
            if not key.startswith('RUNFILES_')
        }
        env.update({
            'EXEC': os.path.abspath(options.executable),
            'OUTPUT_DIR': dataset_dir,
        })
        subprocess.check_call(
            ["bash", "-e", "-c", options.command],
            env=env)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
