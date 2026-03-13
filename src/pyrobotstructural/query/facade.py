from typing import Any

from .nodes import NodesQuery
from .bars import BarsQuery
from .loadcases import CasesQuery
from .combinations import CombinationsQuery
from .model import ModelQuery


class QueryFacade:
    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self.nodes = NodesQuery(self._raw)
        self.bars = BarsQuery(self._raw)
        self.loadcases = CasesQuery(self._raw)
        self.combinations = CombinationsQuery(self._raw)
        self.model = ModelQuery(self._raw)
