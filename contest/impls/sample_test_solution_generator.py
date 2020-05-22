import argparse
import os
import shlex

import jinja2

_SCRIPT_TMPL = """#!/bin/sh

case "${CASE_NAME}" in
{% for file in files -%}
{{ file.name }}) exec cat {{ file.path }};;
{% endfor -%}
*) exit 228;;
esac
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--output_extension', required=True)
    parser.add_argument('files', nargs='*')
    options = parser.parse_args()

    suffix = '.' + options.output_extension

    files = []
    for file in options.files:
        assert file.endswith(suffix)
        files.append({
            'name': shlex.quote(os.path.basename(file[:-len(suffix)])),
            'path': shlex.quote(file),
        })
    script = jinja2.Template(_SCRIPT_TMPL).render(files=files)

    with open(options.output, 'w') as f:
        f.write(script)


if __name__ == '__main__':
    main()
