import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', dest='targets', action='append', required=True)
    parser.add_argument('--workspace', default=os.environ.get('BUILD_WORKSPACE_DIRECTORY', ''))
    options = parser.parse_args()

    with tempfile.NamedTemporaryFile() as event_file:
        args = [
            'bazel',
            'test',
            '--build_event_json_file=%s' % event_file.name,
            '--test_tag_filters=solution',
        ] + options.targets
        subprocess.call(args, cwd=options.workspace, stdout=subprocess.DEVNULL)

        tests = []

        expected_targets = set()

        for line in event_file:
            data = json.loads(line)
            if 'configured' in data:
                if 'solution' in data['configured'].get('tag', []):
                    expected_targets.add(data['id']['targetConfigured']['label'])
                continue
            if 'testResult' not in data:
                continue
            target = data['id']['testResult']['label']
            assert target in expected_targets
            expected_targets.remove(target)
            for output in data['testResult']['testActionOutput']:
                if output['name'] == 'test.outputs__outputs.zip':
                    assert output['uri'].startswith('file://'), output['uri']
                    zip_path = output['uri'][len('file://'):]
                    break
            else:
                tests.append({
                    'target': target,
                    'result': 'error',
                    'message': 'outputs.zip not found',
                })
                continue
            try:
                with zipfile.ZipFile(zip_path) as archive:
                    with archive.open('results.json') as f:
                        test = json.load(f)
            except IOError as e:
                test = {
                    'target': target,
                    'result': 'error',
                    'message': 'Failed to read results.json: %s' % e,
                }
            tests.append(test)

        for target in expected_targets:
            tests.append({
                'target': target,
                'result': 'error',
                'message': 'Test was not run',
            })

    report = {
        'tests': tests,
    }
    json.dump(report, sys.stdout, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
