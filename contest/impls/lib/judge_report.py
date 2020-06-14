import enum
import os
import typing
from typing import Any, Dict, List


class CaseResult(enum.Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    SKIPPED = 'skipped'
    ERROR = 'error'


CaseReport = typing.NamedTuple('CaseReport', [
    ('name', str),
    ('result', CaseResult),
    ('time', float),
    ('message', str),
    ('details', Dict[str, Any]),
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


def to_dict(report: JudgeReport) -> dict:
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


def from_dict(data: dict) -> JudgeReport:
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


def summarize(cases: List[CaseReport], expect: Expect, judge: JudgeInfo) -> JudgeReport:
    for case in cases:
        if case.result not in (CaseResult.ACCEPTED, CaseResult.REJECTED, CaseResult.SKIPPED):
            result = JudgeResult.ERROR
            message = '%s: %s' % (case.name, case.message)
            break
    else:
        if expect == Expect.ACCEPT_ALL:
            for case in cases:
                if case.result == CaseResult.REJECTED:
                    result = JudgeResult.FAILURE
                    message = '%s: %s' % (case.name, case.message)
                    break
            else:
                result = JudgeResult.SUCCESS
                message = 'All accepted'
        elif expect == Expect.REJECT_ANY:
            for case in cases:
                if case.result == CaseResult.REJECTED:
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
