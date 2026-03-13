from typing import Any
from .bootstrap import get_robotom


class _BaseEditor:
    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self._rbt = get_robotom()
