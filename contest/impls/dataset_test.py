import argparse
import os
import subprocess
import sys

from contest.impls import datasets
from contest.impls import exec_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executable', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--command', required=True)
    options = parser.parse_args()

    with datasets.expand(options.dataset) as dataset_dir:
        for case in datasets.cases(dataset_dir):
            print('*** %s: ' % case, end='')
            sys.stdout.flush()

            env = exec_util.make_env({
                'EXEC': os.path.abspath(options.executable),
                'INPUT_DIR': dataset_dir,
                'TESTCASE': case,
            })
            returncode = subprocess.call(
                exec_util.bash_args(options.command),
                env=env)

            if returncode != 0:
                print('FAILED (exit code %d)' % returncode)
                sys.exit(1)
            print('OK')


if __name__ == '__main__':
    main()
