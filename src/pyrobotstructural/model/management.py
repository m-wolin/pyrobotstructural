from typing import Any
from .._base import _BaseEditor

"""This module is meant to handle operations like delate all objects, clear model, multi operation?
Probably very small module"""


class ModelManager(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._cases = self._structure.Cases

    def clear(self, with_loads=True) -> None:
        """Clears (removes) all objects within the model

        Parameters
        ----------
        with_loads: bool, default True
            Trigger if combinations and loadcases shall be cleared as well.
        """
        self._structure.Clear()
        if with_loads:
            comb_selection = self._structure.Selections.CreatePredefined(
                self._rbt.IRobotPredefinedSelection.I_PS_CASE_COMBINATIONS
            )
            self._cases.DeleteMany(comb_selection)
            case_selection = self._structure.Selections.CreatePredefined(
                self._rbt.IRobotPredefinedSelection.I_PS_CASE_SIMPLE_CASES
            )
            self._cases.DeleteMany(case_selection)
