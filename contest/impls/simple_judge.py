import argparse
import os
import subprocess
import sys
import tempfile

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('--answer_extension', required=True)
    parser.add_argument('--expect', default='accept')
    parser.add_argument('solution', nargs=1)
    options = parser.parse_args()

    assert options.expect in ('accept', 'reject_any', 'reject_all')

    with datasets.expand([options.dataset]) as dataset_dir:
        for name in datasets.names(dataset_dir):
            input_path = os.path.join(dataset_dir, name + '.' + options.input_extension)
            if not os.path.exists(input_path):
                continue
            answer_path = os.path.join(dataset_dir, name + '.' + options.answer_extension)
            assert os.path.exists(answer_path), answer_path

            print('------- %s' % name)
            with open(input_path, 'rb') as input_file:
                with tempfile.NamedTemporaryFile() as output_file:
                    subprocess.check_call(
                        [options.solution[0]],
                        stdin=input_file,
                        stdout=output_file)
                    returncode = subprocess.call(
                        [options.comparator, output_file.name, answer_path])
                    if returncode == 0:
                        if options.expect == 'reject_all':
                            print('*** PASS (UNEXPECTED)')
                            sys.exit(1)
                        print('PASS')
                    else:
                        if options.expect == 'accept':
                            print('*** FAIL')
                            sys.exit(1)
                        elif options.expect == 'reject_any':
                            print('*** FAIL (EXPECTED)')
                            sys.exit(0)
                        print('FAIL (EXPECTED)')
                    print()

        if options.expect == 'reject_any':
            print('*** ALL PASS (UNEXPECTED)')
            sys.exit(1)

        print('*** ALL PASS')


if __name__ == '__main__':
    main()
