import argparse
import os
import subprocess
import sys
import time
from typing import List, Tuple

from contest.impls.lib import exec_util
from contest.impls.lib import judge_common


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--judge_name', required=True)
    parser.add_argument('--expect',
                        type=judge_common.Expect,
                        choices=list(judge_common.Expect),
                        default=judge_common.Expect.ACCEPT_ALL)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--exec', required=True)
    parser.add_argument('--command', required=True)
    parser.add_argument('--case_timeout', type=int, required=True)
    parser.add_argument('--timeout_multiplier', type=int, default=1)
    parser.add_argument('solution')
    options = parser.parse_args()

    info = judge_common.JudgeInfo(
        target=options.judge_name,
        type='interactive_judge',
        metadata={},
    )
    timeout = (
            options.case_timeout *
            options.timeout_multiplier *
            int(os.environ.get('JUDGE_TIMEOUT_MULTIPLIER', '1')))
    print('Test target: %s (%s)' % (info.target, info.type))
    print('Per-case timeout: %ds' % timeout)
    print('Expectation: %s' % options.expect.value)

    def _run_case(dataset_dir: str, name: str) -> Tuple[judge_common.CaseReport, List[judge_common.Output]]:
        solution_stderr_path = os.path.join(options.output_dir, '%s.solution.stderr' % name)
        judge_stderr_path = os.path.join(options.output_dir, '%s.judge.stderr' % name)

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
            return judge_common.CaseReport(
                name=name,
                time=run_time,
                result=judge_common.CaseResult.TIMEOUT,
                message='Solution timeout',
                details={
                    'solution_time': run_time,
                    'solution_code': solution_code,
                    'judge_time': run_time,
                    'judge_code': judge_code,
                },
            ), [
                judge_common.Output(title='SOLUTION STDERR', path=solution_stderr_path),
                judge_common.Output(title='JUDGE STDERR', path=judge_stderr_path),
            ]
        elif judge_code != 0:
            return judge_common.CaseReport(
                name=name,
                time=run_time,
                result=judge_common.CaseResult.REJECTED,
                message='Judge exited with code %d' % judge_code,
                details={
                    'solution_time': run_time,
                    'solution_code': solution_code,
                    'judge_time': run_time,
                    'judge_code': judge_code,
                },
            ), [
                judge_common.Output(title='SOLUTION STDERR', path=solution_stderr_path),
                judge_common.Output(title='JUDGE STDERR', path=judge_stderr_path),
            ]

        return judge_common.CaseReport(
            name=name,
            time=run_time,
            result=judge_common.CaseResult.ACCEPTED,
            message='OK',
            details={
                'solution_time': run_time,
                'solution_code': solution_code,
                'judge_time': run_time,
                'judge_code': judge_code,
            },
        ), []

    sys.exit(judge_common.main(info, options.expect, options.output_dir, options.dataset, _run_case))


if __name__ == '__main__':
    main()
