import argparse
import io
import json
import os
import sys
import zipfile

import jinja2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('input')
    options = parser.parse_args()

    known_solution_tests = set()
    broken_tests = {}
    solution_tests = {}
    other_tests = {}

    with open(options.input) as event_file:
        for line in event_file:
            data = json.loads(line)
            if 'configured' in data:
                if 'testSize' in data['configured']:
                    target = data['id']['targetConfigured']['label']
                    broken_tests[target] = {
                        'target': target,
                        'result': 'error',
                        'message': 'Test was not run',
                    }
                    tags = data['configured'].get('tag', [])
                    if 'solution' in tags:
                        known_solution_tests.add(target)
            if 'testResult' in data:
                target = data['id']['testResult']['label']
                if target in known_solution_tests:
                    for output in data['testResult']['testActionOutput']:
                        if output['name'] == 'test.outputs__outputs.zip':
                            assert output['uri'].startswith('file://'), output['uri']
                            zip_path = output['uri'][len('file://'):]
                            break
                    else:
                        broken_tests[target]['message'] = 'outputs.zip not found'
                        continue
                    try:
                        with zipfile.ZipFile(zip_path) as archive:
                            with archive.open('results.json') as f:
                                solution_tests[target] = json.load(io.TextIOWrapper(f))
                                broken_tests.pop(target)
                    except IOError as e:
                        broken_tests[target]['message'] = 'Failed to read results.json: %s' % e
                else:
                    status = data['testResult']['status']
                    result = {
                        'PASSED': 'success',
                        'FAILED': 'failure',
                    }.get(status, 'error')
                    other_tests[target] = {
                        'target': target,
                        'result': result,
                        'message': status,
                    }
                    broken_tests.pop(target)

    judge_matrices = {}
    for test_target, test in sorted(solution_tests.items()):
        judge_target = test['judge']['target']
        judge_matrix = judge_matrices.setdefault(
            judge_target,
            {'judge_target': judge_target, 'test_targets': [], 'cases': {}})
        judge_matrix['test_targets'].append(test_target)
        for case in test['cases']:
            row = judge_matrix['cases'].setdefault(case['name'], {})
            row[test_target] = case

    report = {
        'broken_tests': broken_tests,
        'solution_tests': solution_tests,
        'judge_matrices': judge_matrices,
        'other_tests': other_tests,
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        autoescape=True)
    template = env.get_template('test_results.md')
    html = template.render(report=report)

    if options.output:
        with open(options.output, 'w') as out:
            out.write(html)
    else:
        sys.stdout.write(html)


if __name__ == '__main__':
    main()
