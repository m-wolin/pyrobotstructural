from typing import Any

from .nodes import NodesQuery
from .bars import BarsQuery
from .loadcases import CasesQuery
from .combinations import CombinationsQuery
from .model import ModelQuery
from .results import BarResultsQuery, ShellResultsQuery


class QueryFacade:
    """Read-only facade for querying the model and analysis results.

    Accessed via ``app.query``.  Aggregates query classes for nodes, bars,
    load cases, combinations, model metadata, bar results, and shell results.
    """

    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self.nodes = NodesQuery(self._raw)
        self.bars = BarsQuery(self._raw)
        self.loadcases = CasesQuery(self._raw)
        self.combinations = CombinationsQuery(self._raw)
        self.model = ModelQuery(self._raw)
        self.results = BarResultsQuery(self._raw)
        self.shell_results = ShellResultsQuery(self._raw)
