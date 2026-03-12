import os
from glob import glob

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def resource_filenames() -> list[str]:
    files = glob(os.path.join(_SCRIPT_DIR, "*.*"))
    files = [filename for filename in files if filename != __file__]
    return files
