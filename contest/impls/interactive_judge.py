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
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--command', required=True)
    parser.add_argument('--case_timeout', type=int, required=True)
    parser.add_argument('--timeout_multiplier', type=int, default=1)
    parser.add_argument('solution')
    options = parser.parse_args()

    cases = []

    with datasets.expand(options.dataset) as dataset_dir:
        for name in datasets.cases(dataset_dir):
            if cases and judge_report.may_break(cases[-1], options.expect):
                break

            print('*** %s: ' % name, end='')

            solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % name)
            judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % name)

            timeout = (
                    options.case_timeout *
                    options.timeout_multiplier *
                    int(os.environ.get('JUDGE_TIMEOUT_MULTIPLIER', '1')))

            judge_stdin, solution_stdout = os.pipe()
            solution_stdin, judge_stdout = os.pipe()
            env = exec_util.make_env({
                'EXEC': options.exec,
                'INPUT_DIR': dataset_dir,
                'TESTCASE': name,
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

            try:
                judge_code = judge_proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                judge_proc.kill()
                solution_proc.kill()
                judge_proc.wait()
                judge_code = 111
            try:
                solution_code = solution_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                solution_proc.kill()
                solution_code = solution_proc.wait()

            run_time = time.time() - start_time

            if judge_code == 111:
                msg = 'Solution timeout (%ds)' % timeout
                print(msg)
                print('--- SOLUTION STDERR ---')
                with open(solution_stderr_path, 'r') as f:
                    print(f.read())
                print('--- JUDGE STDERR ---')
                with open(judge_stderr_path, 'r') as f:
                    print(f.read())
                cases.append(judge_report.CaseReport(
                    name=name,
                    time=run_time,
                    result=judge_report.CaseResult.TIMEOUT,
                    message=msg,
                    details={
                        'solution_time': run_time,
                        'solution_code': solution_code,
                        'judge_time': run_time,
                        'judge_code': judge_code,
                    },
                ))
                continue
            elif judge_code != 0:
                msg = 'Judge exited with code %d' % judge_code
                print(msg)
                print('--- SOLUTION STDERR ---')
                with open(solution_stderr_path, 'r') as f:
                    print(f.read())
                print('--- JUDGE STDERR ---')
                with open(judge_stderr_path, 'r') as f:
                    print(f.read())
                cases.append(judge_report.CaseReport(
                    name=name,
                    time=run_time,
                    result=judge_report.CaseResult.REJECTED,
                    message=msg,
                    details={
                        'solution_time': run_time,
                        'solution_code': solution_code,
                        'judge_time': run_time,
                        'judge_code': judge_code,
                    },
                ))
                continue

            msg = 'OK'
            print(msg)
            cases.append(judge_report.CaseReport(
                name=name,
                time=run_time,
                result=judge_report.CaseResult.ACCEPTED,
                message=msg,
                details={
                    'solution_time': run_time,
                    'solution_code': solution_code,
                    'judge_time': run_time,
                    'judge_code': judge_code,
                },
            ))

    info = judge_report.JudgeInfo(
        target=options.judge_name,
        type='interactive_judge',
        metadata={},
    )
    report = judge_report.summarize(cases, options.expect, info)
    with open(os.path.join(options.output_dir, 'results.json'), 'w') as f:
        json.dump(judge_report.to_dict(report), f, indent=2, sort_keys=True)

    if report.result != judge_report.JudgeResult.SUCCESS:
        sys.exit(1)


if __name__ == '__main__':
    main()
