import argparse
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(interactive_judge)s \\
    --output_dir="${TEST_UNDECLARED_OUTPUTS_DIR}" \\
    --judge_name=%(judge_name)s \\
    --dataset=%(dataset)s \\
    --exec=%(exec)s \\
    --command=%(command)s \\
    --case_timeout=%(case_timeout)d \\
    "$@"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--interactive_judge', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--command', required=True)
    parser.add_argument('--case_timeout', type=int, required=True)
    options = parser.parse_args()

    script_vars = {
        'interactive_judge': shlex.quote(options.interactive_judge),
        'judge_name': shlex.quote(options.judge_name),
        'dataset': shlex.quote(options.dataset),
        'exec': shlex.quote(options.exec),
        'command': shlex.quote(options.command),
        'case_timeout': options.case_timeout,
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
