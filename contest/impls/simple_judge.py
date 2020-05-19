import argparse
import json
import os
import shlex
import subprocess
import sys
import time

from contest.impls import datasets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('--answer_extension', required=True)
    parser.add_argument('--expect', default='accept')
    parser.add_argument('solution')
    options = parser.parse_args()

    assert options.expect in ('accept', 'reject_any', 'reject_all')

    with datasets.expand([options.dataset]) as dataset_dir:
        names = datasets.names(dataset_dir)
        tests = []

        for name in names:
            print('======= %s' % name)
            input_path = os.path.join(dataset_dir, name + '.' + options.input_extension)
            if not os.path.exists(input_path):
                tests.append({
                    'name': name,
                    'result': 'error',
                    'message': 'Input file missing: %s' % os.path.basename(input_path),
                })
                continue
            answer_path = os.path.join(dataset_dir, name + '.' + options.answer_extension)
            if not os.path.exists(answer_path):
                tests.append({
                    'name': name,
                    'result': 'error',
                    'message': 'Answer file missing: %s' % os.path.basename(answer_path),
                })
                continue

            solution_stdout_path = os.path.join(options.output_dir, '%s.solution.stdout' % name)
            solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % name)

            with open(input_path, 'r') as stdin_file, \
                    open(solution_stdout_path, 'w+') as stdout_file, \
                    open(solution_stderr_path, 'w+') as stderr_file:
                args = [options.solution]
                print('>>> %s' % ' '.join(shlex.quote(arg) for arg in args))

                start_time = time.time()
                solution_code = subprocess.call(
                    args,
                    stdin=stdin_file,
                    stdout=stdout_file,
                    stderr=stderr_file)
                solution_time = time.time() - start_time

                print('Finished with code %d in %.1fs' % (solution_code, solution_time))
                print('--- STDOUT ---')
                print(stdout_file.read())
                print('--- STDERR ---')
                print(stderr_file.read())

            if solution_code != 0:
                tests.append({
                    'name': name,
                    'result': 'reject',
                    'message': 'Solution exited with code %d' % solution_code,
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                })
                continue

            judge_stdout_path = os.path.join(options.output_dir, '%s.judge.stdout' % name)
            judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % name)

            with open(judge_stdout_path, 'w+') as stdout_file, \
                    open(judge_stderr_path, 'w+') as stderr_file:
                args = [options.comparator, solution_stdout_path, answer_path]
                print('>>> %s' % ' '.join(shlex.quote(arg) for arg in args))

                start_time = time.time()
                judge_code = subprocess.call(
                    args,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_file,
                    stderr=stderr_file)
                judge_time = time.time() - start_time

                print('Finished with code %d in %.1fs' % (judge_code, judge_time))
                print('--- STDOUT ---')
                print(stdout_file.read())
                print('--- STDERR ---')
                print(stderr_file.read())

            if judge_code != 0:
                tests.append({
                    'name': name,
                    'result': 'reject',
                    'message': 'Judge exited with code %d' % judge_code,
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                    'judge_time': judge_time,
                    'judge_code': judge_code,
                })
                continue

            tests.append({
                'name': name,
                'result': 'accept',
                'solution_time': solution_time,
                'solution_code': solution_code,
                'judge_time': judge_time,
                'judge_code': judge_code,
            })

    for test in tests:
        if test['result'] not in ('accept', 'reject'):
            result = 'error'
            message = '%s: %s' % (test['name'], test['message'])
            break
    else:
        if options.expect == 'accept':
            for test in tests:
                if test['result'] == 'reject':
                    result = 'failure'
                    message = '%s: %s' % (test['name'], test['message'])
                    break
            else:
                result = 'success'
                message = 'All accepted'
        elif options.expect == 'reject_any':
            for test in tests:
                if test['result'] == 'reject':
                    result = 'success'
                    message = '%s: Rejected as expected: %s' % (test['name'], test['message'])
                    break
            else:
                result = 'failure'
                message = 'All accepted unexpectedly'
        elif options.expect == 'reject_all':
            for test in tests:
                if test['result'] == 'accept':
                    result = 'failure'
                    message = '%s: Accepted unexpectedly' % test['name']
                    break
            else:
                result = 'success'
                message = 'All rejected'
        else:
            assert False, options.expect

    report = {
        'judge': 'simple_judge',
        'target': os.environ['TEST_TARGET'],
        'expect': options.expect,
        'result': result,
        'message': message,
        'tests': tests,
    }
    with open(os.path.join(options.output_dir, 'results.json'), 'w') as f:
        json.dump(report, f, indent=2, sort_keys=True)

    if result != 'success':
        sys.exit(1)


if __name__ == '__main__':
    main()
