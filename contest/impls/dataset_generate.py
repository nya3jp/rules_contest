import argparse
import os
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--executable', required=True)
    options = parser.parse_args()

    with tempfile.TemporaryDirectory() as dataset_dir:
        env = os.environ.copy()
        env['OUTPUT_DIR'] = dataset_dir
        subprocess.check_call(
            [options.executable],
            env=env)
        subprocess.check_call(
            ['zip', '-q', '-r', os.path.abspath(options.output), '.'],
            cwd=dataset_dir)


if __name__ == '__main__':
    main()
