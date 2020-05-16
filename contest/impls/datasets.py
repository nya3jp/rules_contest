import contextlib
import os
import shutil
import subprocess
import tempfile

from typing import List


@contextlib.contextmanager
def expand(sources: List[str]) -> str:
    with tempfile.TemporaryDirectory() as dataset_dir:
        for source in sources:
            if source.endswith('.zip'):
                subprocess.check_call(
                    ['unzip', '-q', '-n', os.path.abspath(source)],
                    cwd=dataset_dir)
            else:
                shutil.copy(source, os.path.join(dataset_dir, os.path.basename(source)))
        yield dataset_dir


def names(dataset_dir: str) -> List[str]:
    nameset = set()
    for filename in os.listdir(dataset_dir):
        nameset.add(filename.split('.', 2)[0])
    return sorted(nameset)
