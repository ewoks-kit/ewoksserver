import os
import json
from typing import List

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_workflow(name: str) -> List[str]:
    filename = os.path.join(_SCRIPT_DIR, name)
    with open(filename, "rb") as f:
        return json.load(f)
