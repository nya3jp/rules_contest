import argparse
import os
import subprocess

from third_party.runfiles import runfiles

current_repository_root = os.environ['TEST_TARGET'].split('//')[0] + '//'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true')
    options = parser.parse_args()

    resolver = runfiles.Create()
    bin_path = resolver.Rlocation('rules_contest/contest/render_test_results')
    input_path = resolver.Rlocation(
        'rules_contest/tests/render_test_results/testdata/build.jsonl')
    golden_path = resolver.Rlocation(
        'rules_contest/tests/render_test_results/golden.md')

    output = subprocess.check_output(
        [bin_path, input_path],
        encoding='utf-8',
        cwd=os.path.dirname(resolver.Rlocation('rules_contest/tests')),
    )
    output = output.replace(current_repository_root, '//')

    if options.update:
        with open(golden_path, 'w') as f:
            f.write(output)
        return

    subprocess.run(
        ['diff', '-u', '/dev/stdin', golden_path],
        input=output, encoding='utf-8', check=True)


if __name__ == '__main__':
    main()
