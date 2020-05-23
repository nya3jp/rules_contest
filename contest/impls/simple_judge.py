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
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--input_extension', required=True)
    parser.add_argument('--answer_extension', required=True)
    parser.add_argument('--metadata', default='{}')
    parser.add_argument('--expect', default='accepted')
    parser.add_argument('solution')
    options = parser.parse_args()

    assert options.expect in ('accepted', 'reject_any', 'reject_all')
    metadata = json.loads(options.metadata)

    with datasets.expand(options.dataset) as dataset_dir:
        cases = []

        for case in datasets.cases(dataset_dir):
            print('*** %s: ' % case.name, end='')
            input_path = case.files.get(options.input_extension)
            if not input_path:
                msg = 'Input file missing: %s.%s' % (case.name, options.input_extension)
                print(msg)
                cases.append({
                    'name': case.name,
                    'result': 'error',
                    'message': msg,
                })
                continue
            answer_path = case.files.get(options.answer_extension)
            if not answer_path:
                msg = 'Answer file missing: %s.%s' % (case.name, options.answer_extension)
                print(msg)
                cases.append({
                    'name': case.name,
                    'result': 'error',
                    'message': msg,
                })
                continue

            solution_stdout_path = os.path.join(options.output_dir, '%s.solution.stdout' % case.name)
            solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % case.name)

            with open(input_path, 'rb') as stdin_file, \
                    open(solution_stdout_path, 'wb') as stdout_file, \
                    open(solution_stderr_path, 'wb') as stderr_file:
                args = [options.solution]

                env = os.environ.copy()
                env.update(case.env)

                start_time = time.time()
                solution_code = subprocess.call(
                    args,
                    env=env,
                    stdin=stdin_file,
                    stdout=stdout_file,
                    stderr=stderr_file)
                solution_time = time.time() - start_time

            if solution_code == 228:
                msg = 'Solution skipped the test case'
                print(msg)
                cases.append({
                    'name': case.name,
                    'result': 'skipped',
                    'message': msg,
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                })
                continue
            elif solution_code != 0:
                msg = 'Solution exited with code %d' % solution_code
                print(msg)
                print('--- SOLUTION STDOUT ---')
                with open(solution_stdout_path, 'r') as f:
                    print(f.read())
                print('--- SOLUTION STDERR ---')
                with open(solution_stderr_path, 'r') as f:
                    print(f.read())
                cases.append({
                    'name': case.name,
                    'result': 'rejected',
                    'message': msg,
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                })
                continue

            judge_stdout_path = os.path.join(options.output_dir, '%s.judge.stdout' % case.name)
            judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % case.name)

            with open(judge_stdout_path, 'wb') as stdout_file, \
                    open(judge_stderr_path, 'wb') as stderr_file:
                args = [options.comparator, input_path, solution_stdout_path, answer_path]

                env = os.environ.copy()
                env.update(case.env)

                start_time = time.time()
                judge_code = subprocess.call(
                    args,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_file,
                    stderr=stderr_file)
                judge_time = time.time() - start_time

            if judge_code != 0:
                msg = 'Judge exited with code %d' % judge_code
                print(msg)
                print('--- SOLUTION STDOUT ---')
                with open(solution_stdout_path, 'r') as f:
                    print(f.read())
                print('--- SOLUTION STDERR ---')
                with open(solution_stderr_path, 'r') as f:
                    print(f.read())
                print('--- JUDGE STDOUT ---')
                with open(judge_stdout_path, 'r') as f:
                    print(f.read())
                print('--- JUDGE STDERR ---')
                with open(judge_stderr_path, 'r') as f:
                    print(f.read())
                cases.append({
                    'name': case.name,
                    'result': 'rejected',
                    'message': msg,
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                    'judge_time': judge_time,
                    'judge_code': judge_code,
                })
                continue

            msg = 'OK'
            print(msg)
            cases.append({
                'name': case.name,
                'result': 'accepted',
                'message': msg,
                'solution_time': solution_time,
                'solution_code': solution_code,
                'judge_time': judge_time,
                'judge_code': judge_code,
            })

    for case in cases:
        if case['result'] not in ('accepted', 'rejected', 'skipped'):
            result = 'error'
            message = '%s: %s' % (case['name'], case['message'])
            break
    else:
        if options.expect == 'accepted':
            for case in cases:
                if case['result'] == 'rejected':
                    result = 'failure'
                    message = '%s: %s' % (case['name'], case['message'])
                    break
            else:
                result = 'success'
                message = 'All accepted'
        elif options.expect == 'reject_any':
            for case in cases:
                if case['result'] == 'rejected':
                    result = 'success'
                    message = 'Rejected as expected: %s: %s' % (case['name'], case['message'])
                    break
            else:
                result = 'failure'
                message = 'All accepted unexpectedly'
        elif options.expect == 'reject_all':
            for case in cases:
                if case['result'] == 'accepted':
                    result = 'failure'
                    message = 'Accepted unexpectedly: %s' % case['name']
                    break
            else:
                result = 'success'
                message = 'All rejected as expected'
        else:
            assert False, options.expect

    report = {
        'judge': {
            'target': options.judge_name,
            'type': 'simple_judge',
            'metadata': metadata,
        },
        'target': os.environ['TEST_TARGET'],
        'expect': options.expect,
        'result': result,
        'message': message,
        'cases': cases,
    }
    with open(os.path.join(options.output_dir, 'results.json'), 'w') as f:
        json.dump(report, f, indent=2, sort_keys=True)

    if result != 'success':
        sys.exit(1)


if __name__ == '__main__':
    main()
