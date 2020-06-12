import argparse
import json
import os
import subprocess
import sys
import time

from contest.impls.lib import datasets
from contest.impls.lib import exec_util


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--command', required=True)
    parser.add_argument('--metadata', default='{}')
    parser.add_argument('--expect', default='accept_all')
    parser.add_argument('solution')
    options = parser.parse_args()

    assert options.output_dir, '--output_dir empty'
    assert options.expect in ('accept_all', 'reject_any', 'reject_all')
    metadata = json.loads(options.metadata)

    with datasets.expand(options.dataset) as dataset_dir:
        cases = []

        for case in datasets.cases(dataset_dir):
            print('*** %s: ' % case, end='')

            solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % case)
            judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % case)

            judge_stdin, solution_stdout = os.pipe()
            solution_stdin, judge_stdout = os.pipe()
            env = exec_util.make_env({
                'EXEC': options.exec,
                'INPUT_DIR': dataset_dir,
                'TESTCASE': case,
            })

            start_time = time.time()

            with open(judge_stderr_path, 'wb') as judge_stderr:
                judge_proc = subprocess.Popen(
                    exec_util.bash_args(options.command),
                    env=env,
                    stdin=judge_stdin,
                    stdout=judge_stdout,
                    stderr=judge_stderr)

            with open(solution_stderr_path, 'wb') as solution_stderr:
                solution_proc = subprocess.Popen(
                    [options.solution],
                    stdin=solution_stdin,
                    stdout=solution_stdout,
                    stderr=solution_stderr)

            judge_code = judge_proc.wait()
            try:
                solution_code = solution_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                solution_proc.terminate()
                solution_code = solution_proc.wait

            run_time = time.time() - start_time

            if judge_code != 0:
                msg = 'Judge exited with code %d' % judge_code
                print(msg)
                print('--- SOLUTION STDERR ---')
                with open(solution_stderr_path, 'r') as f:
                    print(f.read())
                print('--- JUDGE STDERR ---')
                with open(judge_stderr_path, 'r') as f:
                    print(f.read())
                cases.append({
                    'name': case,
                    'result': 'rejected',
                    'message': msg,
                    'solution_time': run_time,
                    'solution_code': solution_code,
                    'judge_time': run_time,
                    'judge_code': judge_code,
                })
                continue

            msg = 'OK'
            print(msg)
            cases.append({
                'name': case,
                'result': 'accepted',
                'message': msg,
                'solution_time': run_time,
                'solution_code': solution_code,
                'judge_time': run_time,
                'judge_code': judge_code,
            })

    for case in cases:
        if case['result'] not in ('accepted', 'rejected', 'skipped'):
            result = 'error'
            message = '%s: %s' % (case['name'], case['message'])
            break
    else:
        if options.expect == 'accept_all':
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
            'type': 'interactive_judge',
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
