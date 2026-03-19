from typing import Any
from .._base import _BaseEditor


class CombinationsQuery(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def get_all(self, return_objects: bool = True) -> list | Any:
        """
        Gets a list of objects or values depending on the input.

        Parameters
        ----------
        return_objects: bool
            Trigger to return IRobotCaseCombination or list with values

        Returns
        ----------
        IRobotCaseSever or list[name:int, number:int, comb_type: str]
        """
        # TODO: Refactor to use existing enum rather than additional dictionary
        combination_type = {
            0: "ULS",
            1: "SLS",
            2: "ALS",
            3: "SPC",
        }
        all_cases = self._structure.Cases.GetAll()
        lcombs = []
        for i in range(1, all_cases.Count + 1):  # loop1
            lcase = self._rbt.IRobotCase(all_cases.Get(i))
            if int(lcase.Type) == 1:
                lcomb = self._rbt.IRobotCaseCombination(lcase)
                if return_objects:
                    lcombs.append(lcomb)
                else:
                    name = lcomb.Name
                    number = lcomb.Number
                    comb_type = combination_type[int(lcomb.CombinationType)]
                    # TODO: add factors to the returned values
                    lcombs.append([name, number, comb_type])
        return lcombs

    # def get_combination_factors(self, lcomb: Any) -> list:
    #     case_factor_mng = lcomb.CaseFactors
    # TODO: finish factor propagation

    def get_single(self, case_index: int, number: int = None) -> Any:
        """
        Gets combination of given number

        Parameters
        ----------
        case_index: int
            Index for the combination.
        number: int, optional
            Number of the combination, overwrites index.

        Returns
        ----------
        IRobotCase
        """
        all_cases = self._structure.Cases.GetAll()
        if number is not None:
            for i in range(1, all_cases.Count + 1):  # loop1
                lcase = self._rbt.IRobotCase(all_cases.Get(i))
                if lcase.Number == number:
                    return lcase
        else:
            return self._rbt.IRobotCase(all_cases.Get(case_index))
