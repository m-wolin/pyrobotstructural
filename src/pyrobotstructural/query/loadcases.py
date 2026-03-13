from typing import Any
from .._base import _BaseEditor


class CasesQuery(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def get_all_load_cases(self) -> Any:
        """
        Returns
        ----------
        IRobotCaseSever
        """
        return self._structure.Cases.GetAll()

    def get_simple_loadcase(self, case_index: int, number: int = None) -> Any:
        """

        Parameters
        ----------
        case_index: int
            Index for the loadcase.
        number: int, optional
            Number of the loadcase, overwrites index.

        Returns
        ----------
        IRobotCase
            You can provide either index or number of the combination.
        """

        all_cases = self.get_all_load_cases()
        if number is not None:
            for i in range(1, all_cases.Count + 1):  # loop1
                lcase = self._rbt.IRobotCase(all_cases.Get(i))
                if lcase.Number == number:
                    return lcase
        else:
            return self._rbt.IRobotCase(all_cases.Get(case_index))
