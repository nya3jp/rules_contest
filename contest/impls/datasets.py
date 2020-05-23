import contextlib
import os
import subprocess
import tempfile
import zipfile
from typing import Dict, List
import typing


@contextlib.contextmanager
def expand(zip_path: str) -> str:
    with tempfile.TemporaryDirectory() as dataset_dir:
        extract(zip_path, dataset_dir)
        yield dataset_dir


def extract(zip_path: str, out_dir: str) -> None:
    with zipfile.ZipFile(zip_path, 'r') as zf:
        if not zf.namelist():
            return
    subprocess.check_call(
        ['unzip', '-q', '-n', os.path.abspath(zip_path)],
        cwd=out_dir)


Case = typing.NamedTuple(
    'Case',
    [('name', str), ('files', Dict[str, str]), ('env', Dict[str, str])])


def cases(dataset_dir: str) -> List[Case]:
    case_map = {}
    for filename in os.listdir(dataset_dir):
        name, ext = filename.split('.', 2)
        case = case_map.setdefault(name, Case(name=name, files={}, env={'CASE_NAME': name}))
        filepath = os.path.join(dataset_dir, filename)
        case.files[ext] = filepath
        env_name = 'INPUT_%s' % ext.upper().replace('.', '_')
        case.env[env_name] = filepath
    return sorted(case_map.values())


def create(in_dir: str, zip_path: str) -> None:
    if not os.listdir(in_dir):
        with zipfile.ZipFile(zip_path, 'w'):
            pass
        return
    subprocess.check_call(
        ['zip', '-q', '-r', os.path.abspath(zip_path), '.'],
        cwd=in_dir)
