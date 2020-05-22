import argparse
import os

import jinja2
import yaml

from contest.impls import datasets


class LazyDatasetContent:
    def __init__(self, dataset_dir: str):
        self._dataset_dir = dataset_dir

    def __getitem__(self, name: str) -> str:
        try:
            with open(os.path.join(self._dataset_dir, name), 'r') as f:
                return f.read()
        except IOError:
            raise KeyError('file not found: %s' % name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--template_vars_file', action='append')
    options = parser.parse_args()

    template_vars = {}
    for vars_file in options.template_vars_file:
        with open(vars_file, 'r') as f:
            template_vars.update(yaml.safe_load(f))

    with datasets.expand(options.dataset) as dataset_dir:
        template_vars['dataset'] = LazyDatasetContent(dataset_dir)

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(['.'], followlinks=True))
        template = env.get_template(options.input)
        rendered = template.render(**template_vars)

    with open(options.output, 'w') as f:
        f.write(rendered)


if __name__ == '__main__':
    main()
