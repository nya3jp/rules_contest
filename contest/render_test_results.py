import argparse
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

    solution_tests = {}
    other_tests = {}

    with open(options.input) as event_file:
        for line in event_file:
            data = json.loads(line)
            if 'configured' in data:
                if 'testSize' in data['configured']:
                    target = data['id']['targetConfigured']['label']
                    tags = data['configured'].get('tag', [])
                    tests = solution_tests if 'solution' in tags else other_tests
                    tests[target] = {
                        'target': target,
                        'result': 'error',
                        'message': 'Test was not run',
                    }
            if 'testResult' in data:
                target = data['id']['testResult']['label']
                if target in other_tests:
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
                else:
                    for output in data['testResult']['testActionOutput']:
                        if output['name'] == 'test.outputs__outputs.zip':
                            assert output['uri'].startswith('file://'), output['uri']
                            zip_path = output['uri'][len('file://'):]
                            break
                    else:
                        solution_tests[target] = {
                            'target': target,
                            'result': 'error',
                            'message': 'outputs.zip not found',
                        }
                        continue
                    try:
                        with zipfile.ZipFile(zip_path) as archive:
                            with archive.open('results.json') as f:
                                solution_tests[target] = json.load(f)
                    except IOError as e:
                        solution_tests[target] = {
                            'target': target,
                            'result': 'error',
                            'message': 'Failed to read results.json: %s' % e,
                        }

    report = {
        'solution_tests': solution_tests,
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
