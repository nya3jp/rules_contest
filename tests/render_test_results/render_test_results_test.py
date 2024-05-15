import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true')
    options = parser.parse_args()

    output = subprocess.check_output(
        ['contest/render_test_results', 'tests/render_test_results/testdata/build.jsonl'])
    if options.update:
        with open('tests/render_test_results/golden.md', 'wb') as f:
            f.write(output)
        return

    subprocess.run(
        ['diff', '-u', '/dev/stdin', 'tests/render_test_results/golden.md'],
        input=output, check=True)


if __name__ == '__main__':
    main()
