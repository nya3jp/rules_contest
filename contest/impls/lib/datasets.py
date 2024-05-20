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
        zf.extractall(out_dir)


def cases(dataset_dir: str) -> List[str]:
    return sorted(set(
        filename.split('.', 2)[0]
        for filename in os.listdir(dataset_dir)))


def create(in_dir: str, zip_path: str) -> None:
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for abs_dir, _, files in os.walk(in_dir):
            rel_dir = os.path.relpath(abs_dir, in_dir)
            for file in sorted(files):
                zf.write(
                    os.path.join(abs_dir, file),
                    os.path.join(rel_dir, file))
