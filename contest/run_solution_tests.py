import json
import os
import subprocess
import sys
import tempfile
import zipfile


def main():
    extra_args = sys.argv[1:]
    workspace_dir = os.environ['BUILD_WORKSPACE_DIRECTORY']

    with tempfile.NamedTemporaryFile() as event_file:
        args = [
            'bazel',
            'test',
            '--build_event_json_file=%s' % event_file.name,
            '--test_tag_filters=solution',
        ] + extra_args
        subprocess.call(args, cwd=workspace_dir, stdout=subprocess.DEVNULL)

        tests = []

        for line in event_file:
            data = json.loads(line)
            if 'testResult' not in data:
                continue
            target = data['id']['testResult']['label']
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

    report = {
        'tests': tests,
    }
    json.dump(report, sys.stdout, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
