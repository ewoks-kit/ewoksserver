"""Start ewoks server from the command line

..code: bash

    ewoks-server --reload
"""

import sys
from typing import Optional, List
from uvicorn.main import main as _main


def main(argv: Optional[List[str]] = None) -> None:
    """Exposes the uvicorn CLI with a default APP factory"""
    if argv is None:
        argv = sys.argv[1:]
    if "--factory" not in argv:
        argv += ["--factory", "ewoksserver.app:create_app"]
    _main(argv)


if __name__ == "__main__":
    main()
