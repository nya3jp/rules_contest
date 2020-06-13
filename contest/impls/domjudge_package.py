import argparse
import os
import shutil
import tempfile

import yaml

from contest.impls.lib import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--domjudge_metadata')
    parser.add_argument('--icpc_metadata')
    parser.add_argument('--statements', action='append', default=[])
    parser.add_argument('--dataset', required=True)
    options = parser.parse_args()

    # DOMJudge problem format:
    # https://www.domjudge.org/docs/manual/problem-format.html
    with tempfile.TemporaryDirectory() as tmp_dir:
        if options.domjudge_metadata:
            shutil.copy(
                options.domjudge_metadata,
                os.path.join(tmp_dir, 'domjudge-problem.ini'))

        if options.icpc_metadata:
            shutil.copy(
                options.icpc_metadata,
                os.path.join(tmp_dir, 'problem.yaml'))

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
