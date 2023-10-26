import asyncio
from typing import List, Any

from ..app.routes.execution import socketio


class SocketIOTestClient:
    def __init__(self):
        self._manager = socketio._MANAGER

    def __enter__(self) -> "SocketIOTestClient":
        self._manager.testing = True
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()
        self._manager.testing = False

    def connect(self) -> None:
        return _run_coroutine(self._manager.connect(None, None, None))

    def disconnect(self) -> None:
        return _run_coroutine(self._manager.disconnect(None))

    def get_events(self) -> List[dict]:
        events, self._manager.events = self._manager.events, list()
        return events

    def is_running(self) -> bool:
        return _run_coroutine(self._manager.is_running())


def _run_coroutine(coroutine) -> Any:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)
