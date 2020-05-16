import argparse
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(judge)s \\
    %(judge_args)s \\
    -- \\
    %(solution)s \\
    "$@"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--judge', required=True)
    parser.add_argument('--solution', required=True)
    parser.add_argument('judge_args', nargs='*')
    options = parser.parse_args()

    script_vars = {
        'judge': shlex.quote(options.judge),
        'judge_args': ' '.join(shlex.quote(arg) for arg in options.judge_args),
        'solution': shlex.quote(options.solution),
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
