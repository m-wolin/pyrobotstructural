from typing import Any
from .._base import _BaseEditor
from ..enums import CaseNature, CaseAnalizeType, CombinationType


class CombinationManager(_BaseEditor):
    """Manager for creating ULS and SLS load combinations.

    Accessed via ``app.loads.combinations``.
    """

    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._cases = self._structure.Cases

    def del_all_combinations(self) -> None:
        """Deletes all combinations in the model"""
        comb_selection = self._structure.Selections.CreatePredefined(
            self._rbt.IRobotPredefinedSelection.I_PS_CASE_COMBINATIONS
        )
        self._cases.DeleteMany(comb_selection)

    def add_combination(
        self,
        comb_number: int,
        comb_name: str,
        label: str,
        comb_type: CombinationType,
        case_analize_type: CaseAnalizeType,
        factors: list[tuple],
        case_nature: CaseNature,
        kmatrix: bool = False,
        pdelta: bool = False,
    ) -> None:
        """Creates simple loadcase

        Parameters
        ----------
            comb_number: int, optional
                Number for the load combination - optional, if no input then Free Nuber used
            name: str
                Name for the load combination
            comb_type: enum CombinationType
                Combination type (IRobotCombinationType)
            comb_analize_type: enum CaseAnalizeType
                AnalizeType enum (IRobotCaseAnalizeType)
            factors: list[tuple]
                factors in format: [(case_number, factor), (case_number, factor)...]
            comb_nature: CaseNature
                Nature of the loadcase enum (IRobotCaseNature). Defaults to I_CN_EXPLOATATION.
            kmatrix: bool, optional
                trigger MatrixUpdateAfterEachIteration option
            pdelta:bool, optional
                trigger p-delta
        """
        combination = self._cases.CreateCombination(
            comb_number, comb_name, comb_type, case_nature, case_analize_type
        )
        if label is None or len(label) <= 0:
            combination.label = str(comb_number)
        else:
            combination.label = label
        if kmatrix or pdelta:
            params = self._rbt.IRobotNonlinearAnalysisParams(
                combination.GetAnalysisParams()
            )
            if kmatrix:
                params.MatrixUpdateAfterEachIteration = True
            if pdelta:
                params.PDelta = True
            combination.SetAnalysisParams(params)
        # Apply factors
        case_factor_mng = combination.CaseFactors
        for pair in factors:
            case_factor_mng.New(int(pair[0]), pair[1])
