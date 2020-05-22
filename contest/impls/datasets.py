import contextlib
import os
import subprocess
import tempfile
from typing import List


@contextlib.contextmanager
def expand(zip_path: str) -> str:
    with tempfile.TemporaryDirectory() as dataset_dir:
        extract(zip_path, dataset_dir)
        yield dataset_dir


def extract(zip_path: str, out_dir: str) -> None:
    subprocess.check_call(
        ['unzip', '-q', '-n', os.path.abspath(zip_path)],
        cwd=out_dir)


def names(dataset_dir: str) -> List[str]:
    nameset = set()
    for filename in os.listdir(dataset_dir):
        nameset.add(filename.split('.', 2)[0])
    return sorted(nameset)


def create(in_dir: str, zip_path: str) -> None:
    subprocess.check_call(
        ['zip', '-q', '-r', os.path.abspath(zip_path), '.'],
        cwd=in_dir)
