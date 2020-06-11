import argparse
import os
import subprocess

from contest.impls.lib import datasets
from contest.impls.lib import exec_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--command', required=True)
    options = parser.parse_args()

    with datasets.expand(options.dataset) as dataset_dir:
        for case in datasets.cases(dataset_dir):
            env = exec_util.make_env({
                'EXEC': os.path.abspath(options.executable),
                'INPUT_DIR': dataset_dir,
                'OUTPUT_DIR': dataset_dir,
                'TESTCASE': case,
            })
            subprocess.check_call(
                exec_util.bash_args(options.command),
                env=env)
        datasets.create(dataset_dir, options.output)


if __name__ == '__main__':
    main()
