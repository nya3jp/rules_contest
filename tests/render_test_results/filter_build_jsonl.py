import io
import json
import os
import shutil
import sys
from typing import Any, Optional
import zipfile


_TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'testdata')


def _filter_results(data: Any) -> Any:
    if data is None:
        return data
    if isinstance(data, float):
        return 0
    if isinstance(data, list):
        return [_filter_results(elem) for elem in data]
    if isinstance(data, dict):
        return {key: _filter_results(value) for key, value in data.items()}
    return data


def _process_output_zip(uri: str) -> str:
    assert uri.startswith('file:///')
    src = uri[len('file://'):]
    rel = src.rsplit('/subtests/', 2)[1]
    dst = os.path.join(_TESTDATA_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with zipfile.ZipFile(src, 'r') as src_zip:
        with zipfile.ZipFile(dst, 'w') as dst_zip:
            for name in sorted(src_zip.namelist()):
                with src_zip.open(name, 'r') as src_file:
                    with dst_zip.open(name, 'w') as dst_file:
                        if name == 'results.json':
                            data = json.load(io.TextIOWrapper(src_file))
                            data = _filter_results(data)
                            json.dump(data, io.TextIOWrapper(dst_file), sort_keys=True, indent=2)
                        else:
                            shutil.copyfileobj(src_file, dst_file)
    return 'file://./' + os.path.join('tests/render_test_results/testdata', rel)


def _filter_event(data: dict) -> Optional[dict]:
    if 'testSize' in data.get('configured', {}):
        return {
            'id': {'targetConfigured': {'label': data['id']['targetConfigured']['label']}},
            'configured': {
                'testSize': data['configured']['testSize'],
                'tag': data['configured'].get('tag', []),
            },
        }
    if 'testResult' in data:
        return {
            'id': {'testResult': {'label': data['id']['testResult']['label']}},
            'testResult': {
                'status': data['testResult']['status'],
                'testActionOutput': [
                    {
                        'name': entry['name'],
                        'uri': _process_output_zip(entry['uri']),
                    }
                    for entry in data['testResult']['testActionOutput']
                    if entry['name'] == 'test.outputs__outputs.zip'
                ],
            },
        }
    return None


def main():
    for line in sys.stdin:
        data = json.loads(line)
        data = _filter_event(data)
        if data:
            json.dump(data, sys.stdout, sort_keys=True, separators=(',', ':'))
            sys.stdout.write('\n')


if __name__ == '__main__':
    main()
