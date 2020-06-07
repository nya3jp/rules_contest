import argparse
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(dataset_test)s \\
    --executable=%(executable)s \\
    --dataset=%(dataset)s \\
    --command=%(command)s
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--dataset_test', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--command', required=True)
    options = parser.parse_args()

    script_vars = {
        'dataset_test': shlex.quote(options.dataset_test),
        'executable': shlex.quote(options.executable),
        'dataset': shlex.quote(options.dataset),
        'command': shlex.quote(options.command),
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
