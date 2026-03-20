from typing import Any
from .cases import LoadCaseManager
from .combinations import CombinationManager
from .load import LoadEditor


class LoadsFacade:
    """Facade for managing load cases, combinations, and applied loads.

    Accessed via ``app.loads``.  Aggregates the load case, combination,
    and load application sub-editors.
    """

    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self.load = LoadEditor(self._raw)
        self.cases = LoadCaseManager(self._raw)
        self.combinations = CombinationManager(self._raw)
