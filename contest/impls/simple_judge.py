import argparse
import json
import os
import subprocess
import sys
import time

from contest.impls.lib import datasets
from contest.impls.lib import exec_util
from contest.impls.lib import judge_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--expect',
                        type=judge_report.Expect,
                        choices=list(judge_report.Expect),
                        default=judge_report.Expect.ACCEPT_ALL)
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--solution_command', required=True)
    parser.add_argument('--comparator_command', required=True)
    parser.add_argument('solution')
    options = parser.parse_args()

    cases = []

    with datasets.expand(options.dataset) as dataset_dir:
        for name in datasets.cases(dataset_dir):
            print('*** %s: ' % name, end='')

            solution_output_path = os.path.join(options.output_dir, '%s.solution.output' % name)

            solution_stdout_path = os.path.join(options.output_dir, '%s.solution.stdout' % name)
            solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % name)

            with open(solution_stdout_path, 'wb') as stdout_file, \
                    open(solution_stderr_path, 'wb') as stderr_file:
                env = exec_util.make_env({
                    'EXEC': options.solution,
                    'INPUT_DIR': dataset_dir,
                    'TESTCASE': name,
                    'OUTPUT_FILE': solution_output_path,
                })
                start_time = time.time()
                solution_code = subprocess.call(
                    exec_util.bash_args(options.solution_command),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_file,
                    stderr=stderr_file)
                solution_time = time.time() - start_time

            if solution_code == 228:
                msg = 'Solution skipped the test case'
                print(msg)
                cases.append(judge_report.CaseReport(
                    name=name,
                    time=solution_time,
                    result=judge_report.CaseResult.SKIPPED,
                    message=msg,
                    details={
                        'solution_time': solution_time,
                        'solution_code': solution_code,
                    }
                ))
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
                cases.append(judge_report.CaseReport(
                    name=name,
                    time=solution_time,
                    result=judge_report.CaseResult.REJECTED,
                    message=msg,
                    details={
                        'solution_time': solution_time,
                        'solution_code': solution_code,
                    }
                ))
                continue

            judge_stdout_path = os.path.join(options.output_dir, '%s.judge.stdout' % name)
            judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % name)

            with open(judge_stdout_path, 'wb') as stdout_file, \
                    open(judge_stderr_path, 'wb') as stderr_file:
                env = exec_util.make_env({
                    'EXEC': options.comparator,
                    'INPUT_DIR': dataset_dir,
                    'TESTCASE': name,
                    'OUTPUT_FILE': solution_output_path,
                })
                start_time = time.time()
                judge_code = subprocess.call(
                    exec_util.bash_args(options.comparator_command),
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
                cases.append(judge_report.CaseReport(
                    name=name,
                    time=solution_time,
                    result=judge_report.CaseResult.REJECTED,
                    message=msg,
                    details={
                        'solution_time': solution_time,
                        'solution_code': solution_code,
                        'judge_time': judge_time,
                        'judge_code': judge_code,
                    }
                ))
                continue

            msg = 'OK'
            print(msg)
            cases.append(judge_report.CaseReport(
                name=name,
                time=solution_time,
                result=judge_report.CaseResult.ACCEPTED,
                message=msg,
                details={
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                    'judge_time': judge_time,
                    'judge_code': judge_code,
                }
            ))

    info = judge_report.JudgeInfo(
        target=options.judge_name,
        type='simple_judge',
        metadata={},
    )
    report = judge_report.summarize(cases, options.expect, info)
    with open(os.path.join(options.output_dir, 'results.json'), 'w') as f:
        json.dump(judge_report.to_dict(report), f, indent=2, sort_keys=True)

    if report.result != judge_report.JudgeResult.SUCCESS:
        sys.exit(1)


if __name__ == '__main__':
    main()
