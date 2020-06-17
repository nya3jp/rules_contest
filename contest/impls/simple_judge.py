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
    parser.add_argument('--comparator', required=True)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--solution_command', required=True)
    parser.add_argument('--comparator_command', required=True)
    parser.add_argument('--case_timeout', type=int, required=True)
    parser.add_argument('--timeout_multiplier', type=int, default=1)
    parser.add_argument('solution')
    options = parser.parse_args()

    info = judge_common.JudgeInfo(
        target=options.judge_name,
        type='simple_judge',
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
            try:
                solution_code = subprocess.call(
                    exec_util.bash_args(options.solution_command),
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    timeout=timeout)
            except subprocess.TimeoutExpired:
                solution_code = 111
            solution_time = time.time() - start_time

        if solution_code == 111:
            return judge_common.CaseReport(
                name=name,
                time=solution_time,
                result=judge_common.CaseResult.TIMEOUT,
                message='Solution timeout',
                details={
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                },
            ), []
        if solution_code == 112:
            return judge_common.CaseReport(
                name=name,
                time=solution_time,
                result=judge_common.CaseResult.SKIPPED,
                message='Skipped',
                details={
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                },
            ), []
        if solution_code != 0:
            return judge_common.CaseReport(
                name=name,
                time=solution_time,
                result=judge_common.CaseResult.REJECTED,
                message='Solution exited with code %d' % solution_code,
                details={
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                },
            ), [
                judge_common.Output(title='SOLUTION STDOUT', path=solution_stdout_path),
                judge_common.Output(title='SOLUTION STDERR', path=solution_stderr_path),
            ]

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
            return judge_common.CaseReport(
                name=name,
                time=solution_time,
                result=judge_common.CaseResult.REJECTED,
                message='Judge exited with code %d' % judge_code,
                details={
                    'solution_time': solution_time,
                    'solution_code': solution_code,
                    'judge_time': judge_time,
                    'judge_code': judge_code,
                },
            ), [
                judge_common.Output(title='SOLUTION OUTPUT', path=solution_output_path),
                judge_common.Output(title='SOLUTION STDOUT', path=solution_stdout_path),
                judge_common.Output(title='SOLUTION STDERR', path=solution_stderr_path),
                judge_common.Output(title='JUDGE STDOUT', path=judge_stdout_path),
                judge_common.Output(title='JUDGE STDERR', path=judge_stderr_path),
            ]

        return judge_common.CaseReport(
            name=name,
            time=solution_time,
            result=judge_common.CaseResult.ACCEPTED,
            message='OK',
            details={
                'solution_time': solution_time,
                'solution_code': solution_code,
                'judge_time': judge_time,
                'judge_code': judge_code,
            },
        ), []

    sys.exit(judge_common.main(info, options.expect, options.output_dir, options.dataset, _run_case))


if __name__ == '__main__':
    main()
