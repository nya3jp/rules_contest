import argparse
import os
import shutil
import tempfile

import yaml

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--metadata', required=True)
    parser.add_argument('--statements', action='append')
    parser.add_argument('--dataset', required=True)
    options = parser.parse_args()

    # DOMJudge problem format:
    # https://www.domjudge.org/docs/manual/problem-format.html
    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(options.metadata, 'r') as f:
            # Make sure the metadata YAML is well-formed.
            yaml.safe_load(f)
        shutil.copy(options.metadata, os.path.join(tmp_dir, 'problem.yaml'))

        for statement in options.statements:
            assert statement.endswith(('.html', '.pdf'))
            statement_ext = statement.split('.')[-1]
            shutil.copy(
                statement,
                os.path.join(tmp_dir, 'problem.%s' % statement_ext))

        dataset_dir = os.path.join(tmp_dir, 'data', 'secret')
        os.makedirs(dataset_dir)
        datasets.extract(options.dataset, dataset_dir)

        # TODO: Do not reuse datasets.create to create a problem ZIP archive.
        datasets.create(tmp_dir, options.output)


if __name__ == '__main__':
    main()
