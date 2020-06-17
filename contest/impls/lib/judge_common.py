import enum
import json
import os
import shutil
import sys
import typing
from typing import Any, Dict, List, Tuple

from contest.impls.lib import datasets


class CaseResult(enum.Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    TIMEOUT = 'timeout'
    ERROR = 'error'
    SKIPPED = '_skipped'  # invalid in data


CaseReport = typing.NamedTuple('CaseReport', [
    ('name', str),
    ('result', CaseResult),
    ('time', float),
    ('message', str),
    ('details', Dict[str, Any]),
])


Output = typing.NamedTuple('Output', [
    ('title', str),
    ('path', str),
])


class JudgeResult(enum.Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
    ERROR = 'error'


JudgeInfo = typing.NamedTuple('JudgeInfo', [
    ('target', str),
    ('type', str),
    ('metadata', Dict[str, Any]),
])


class Expect(enum.Enum):
    ACCEPT_ALL = 'accept_all'
    REJECT_ANY = 'reject_any'
    REJECT_ALL = 'reject_all'
    TIMEOUT_ANY = 'timeout_any'

    def __str__(self) -> str:
        return self.value


JudgeReport = typing.NamedTuple('JudgeReport', [
    ('judge', JudgeInfo),
    ('target', str),
    ('expect', Expect),
    ('result', JudgeResult),
    ('message', str),
    ('cases', List[CaseReport]),
])


def _report_to_dict(report: JudgeReport) -> dict:
    return {
        'judge': {
            'target': report.judge.target,
            'type': report.judge.type,
            'metadata': report.judge.metadata,
        },
        'target': report.target,
        'expect': report.expect.value,
        'result': report.result.value,
        'message': report.message,
        'cases': [
            {
                'name': case.name,
                'result': case.result.value,
                'time': case.time,
                'message': case.message,
                'details': case.details,
            }
            for case in report.cases
        ],
    }


def _report_from_dict(data: dict) -> JudgeReport:
    return JudgeReport(
        judge=JudgeInfo(
            target=data['judge']['target'],
            type=data['judge']['type'],
            metadata=data['judge'].get('metadata', {}),
        ),
        target=data['target'],
        expect=Expect(data['expect']),
        result=JudgeResult(data['result']),
        message=data['message'],
        cases=[
            CaseReport(
                name=case['name'],
                result=CaseResult(case['result']),
                time=case['time'],
                message=case['message'],
                details=case.get('details', {}),
            )
            for case in data['cases']
        ],
    )


def _summarize(cases: List[CaseReport], expect: Expect, judge: JudgeInfo) -> JudgeReport:
    for case in cases:
        if case.result == CaseResult.ERROR:
            result = JudgeResult.ERROR
            message = '%s: %s' % (case.name, case.message)
            break
    else:
        if expect == Expect.ACCEPT_ALL:
            for case in cases:
                if case.result != CaseResult.ACCEPTED:
                    result = JudgeResult.FAILURE
                    message = '%s: %s' % (case.name, case.message)
                    break
            else:
                result = JudgeResult.SUCCESS
                message = 'All accepted'
        elif expect == Expect.REJECT_ANY:
            for case in cases:
                if case.result != CaseResult.ACCEPTED:
                    result = JudgeResult.SUCCESS
                    message = 'Rejected as expected: %s: %s' % (case.name, case.message)
                    break
            else:
                result = JudgeResult.FAILURE
                message = 'All accepted unexpectedly'
        elif expect == Expect.REJECT_ALL:
            for case in cases:
                if case.result == CaseResult.ACCEPTED:
                    result = JudgeResult.FAILURE
                    message = 'Accepted unexpectedly: %s' % case.name
                    break
            else:
                result = JudgeResult.SUCCESS
                message = 'All rejected as expected'
        elif expect == Expect.TIMEOUT_ANY:
            for case in cases:
                if case.result == CaseResult.TIMEOUT:
                    result = JudgeResult.SUCCESS
                    message = 'Timeout as expected: %s: %s' % (case.name, case.message)
                    break
            else:
                result = JudgeResult.FAILURE
                message = 'All finished unexpectedly'
        else:
            assert False, expect

    return JudgeReport(
        judge=judge,
        target=os.environ['TEST_TARGET'],
        expect=expect,
        result=result,
        message=message,
        cases=cases,
    )


def _may_break(last_case: CaseReport, expect: Expect) -> bool:
    null_info = JudgeInfo(
        target='',
        type='',
        metadata={},
    )
    init_result = _summarize([], expect, null_info).result
    last_result = _summarize([last_case], expect, null_info).result
    return last_result != init_result


_RULER = '#' * 16
_OUTPUT_BEGIN = '>' * 7
_OUTPUT_END = '<' * 7
RunCaseFunc = typing.Callable[[str, str], Tuple[CaseReport, List[Output]]]


def main(info: JudgeInfo, expect: Expect, output_dir: str, dataset_path: str, run_case: RunCaseFunc) -> int:
    cases = []
    with datasets.expand(dataset_path) as dataset_dir:
        names = datasets.cases(dataset_dir)
        for i, name in enumerate(names):
            print('\n%s %s [%d/%d]' % (_RULER, name, i + 1, len(names)))
            case, outputs = run_case(dataset_dir, name)
            print('Result: %s' % case.result.value)
            print('Runtime: %.1fs' % case.time)
            print('Message: %s' % case.message)
            if outputs:
                print()
            for output in outputs:
                print('%s %s BEGIN' % (_OUTPUT_BEGIN, output.title))
                with open(output.path, 'r') as f:
                    shutil.copyfileobj(f, sys.stdout)
                print('%s %s END' % (_OUTPUT_END, output.title))
            if case.result == CaseResult.SKIPPED:
                continue
            cases.append(case)
            if _may_break(case, expect):
                break

    print('\n%s %s' % (_RULER, 'END'))

    report = _summarize(cases, expect, info)
    with open(os.path.join(output_dir, 'results.json'), 'w') as f:
        json.dump(_report_to_dict(report), f, indent=2, sort_keys=True)

    print('Overall result: %s' % report.result.value)

    if report.result != JudgeResult.SUCCESS:
        return 1
    return 0
