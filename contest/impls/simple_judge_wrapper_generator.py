import argparse
import json
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(simple_judge)s \\
    --output_dir="${TEST_UNDECLARED_OUTPUTS_DIR}" \\
    --judge_name=%(judge_name)s \\
    --comparator=%(comparator)s \\
    --dataset=%(dataset)s \\
    --solution_command=%(solution_command)s \\
    --comparator_command=%(comparator_command)s \\
    "$@"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--simple_judge', required=True)
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--solution_command', required=True)
    parser.add_argument('--comparator_command', required=True)
    options = parser.parse_args()

    script_vars = {
        'simple_judge': shlex.quote(options.simple_judge),
        'judge_name': shlex.quote(options.judge_name),
        'comparator': shlex.quote(options.comparator),
        'dataset': shlex.quote(options.dataset),
        'solution_command': shlex.quote(options.solution_command),
        'comparator_command': shlex.quote(options.comparator_command),
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
