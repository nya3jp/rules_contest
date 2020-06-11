import argparse
import os
import subprocess
import tempfile

from contest.impls.lib import datasets
from contest.impls.lib import exec_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--command', required=True)
    options = parser.parse_args()

    with tempfile.TemporaryDirectory() as dataset_dir:
        env = exec_util.make_env({
            'EXEC': os.path.abspath(options.executable),
            'OUTPUT_DIR': dataset_dir,
        })
        subprocess.check_call(
            exec_util.bash_args(options.command),
            env=env)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
