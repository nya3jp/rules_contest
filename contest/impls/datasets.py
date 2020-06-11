import contextlib
import os
import subprocess
import tempfile
import zipfile
from typing import List


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


def cases(dataset_dir: str) -> List[str]:
    return sorted(set(
        filename.split('.', 2)[0]
        for filename in os.listdir(dataset_dir)))


def create(in_dir: str, zip_path: str) -> None:
    if not os.listdir(in_dir):
        with zipfile.ZipFile(zip_path, 'w'):
            pass
        return
    subprocess.check_call(
        ['zip', '-q', '-r', os.path.abspath(zip_path), '.'],
        cwd=in_dir)
