import argparse
import contextlib
import os
from typing import Optional

import jinja2
import yaml

from contest.impls.lib import datasets


class _LazyDatasetDict:
    def __init__(self, dataset_dir: str):
        self._dataset_dir = dataset_dir

    def __getitem__(self, name: str) -> str:
        try:
            with open(os.path.join(self._dataset_dir, name), 'r') as f:
                return f.read()
        except IOError:
            raise KeyError('file not found: %s' % name)


@contextlib.contextmanager
def _maybe_dataset_dict(zip_path: Optional[str]) -> Optional[_LazyDatasetDict]:
    if not zip_path:
        yield None
    else:
        with datasets.expand(zip_path) as dataset_dir:
            yield _LazyDatasetDict(dataset_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--file', dest='files', action='append')
    parser.add_argument('--vars', dest='vars', action='append')
    parser.add_argument('--dataset')
    options = parser.parse_args()

    template_vars = {
        'files': {},
        'vars': {},
        'dataset': None,
    }
    for paths in options.files:
        for path in paths.split():
            with open(path, 'r') as f:
                template_vars['files'][os.path.basename(path)] = f.read()
    for paths in options.vars:
        for path in paths.split():
            with open(path, 'r') as f:
                template_vars['vars'].update(yaml.safe_load(f))

    with _maybe_dataset_dict(options.dataset) as dataset:
        template_vars['dataset'] = dataset

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(['.'], followlinks=True))
        template = env.get_template(options.input)
        rendered = template.render(**template_vars)

    with open(options.output, 'w') as f:
        f.write(rendered)


if __name__ == '__main__':
    main()
