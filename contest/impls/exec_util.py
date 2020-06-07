import os
from typing import Dict, List


def bash_args(cmd: str) -> List[str]:
    return ["bash", "-e", "-c", cmd]


def make_env(extra_env: Dict[str, str]) -> Dict[str, str]:
    env = os.environ.copy()
    # Remove RUNFILES_ variables so as not to confuse the executable.
    env = {
        key: value
        for key, value in env.items()
        if not key.startswith('RUNFILES_')
    }
    env.update(extra_env)
    return env
