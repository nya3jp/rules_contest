import argparse
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(dataset_test)s \\
    --executable=%(executable)s \\
    --input_extension=%(input_extension)s \\
    %(datasets)s
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--dataset_test', required=True)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('datasets', nargs='*')
    options = parser.parse_args()

    script_vars = {
        'dataset_test': shlex.quote(options.dataset_test),
        'executable': shlex.quote(options.executable),
        'input_extension': shlex.quote(options.input_extension),
        'datasets': ' '.join(shlex.quote(dataset) for dataset in options.datasets),
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
