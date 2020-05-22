import argparse
import json
import shlex

_SCRIPT_TMPL = """#!/bin/sh

exec %(simple_judge)s \\
    --output_dir="${TEST_UNDECLARED_OUTPUTS_DIR}" \\
    --judge_name=%(judge_name)s \\
    --comparator=%(comparator)s \\
    --dataset=%(dataset)s \\
    --input_extension=%(input_extension)s \\
    --answer_extension=%(answer_extension)s \\
    --metadata=%(metadata)s \\
    "$@"
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--simple_judge', required=True)
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('--answer_extension', required=True)
    parser.add_argument('--metadata', action='append', default=[])
    options = parser.parse_args()

    metadata = {}
    for kv in options.metadata:
        k, v = kv.split(':', 1)
        metadata[k] = v

    script_vars = {
        'simple_judge': shlex.quote(options.simple_judge),
        'judge_name': shlex.quote(options.judge_name),
        'comparator': shlex.quote(options.comparator),
        'dataset': shlex.quote(options.dataset),
        'input_extension': shlex.quote(options.input_extension),
        'answer_extension': shlex.quote(options.answer_extension),
        'metadata': shlex.quote(json.dumps(metadata, separators=(',', ':'), sort_keys=True)),
    }
    script = _SCRIPT_TMPL % script_vars

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
