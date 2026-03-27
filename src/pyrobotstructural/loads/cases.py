from typing import Any
from .._base import _BaseEditor
from ..enums import CaseNature, CaseAnalizeType


class LoadCaseManager(_BaseEditor):
    """Manager for creating and listing load cases.

    Accessed via ``app.loads.cases``.
    """

    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._cases = self._structure.Cases

    def add_loadcase(
        self,
        name: str,
        nature: CaseNature,
        analize_type: CaseAnalizeType,
        number: int = None,
        auxillary: bool = False,
        kmatrix: bool = False,
        pdelta: bool = False,
        label: str = None,
    ) -> None:
        """
        Creates simple loadcase.

        Parameters
        ----------
            name: str
                Name for the loadcase
            nature: CaseNature
                Nature of the loadcase enum
            analize_type: enum CaseAnalizeType
                AnalizeType enum (IRobotCaseAnalizeType)
            number: int, optional
                Number of the loadcase - optional, if no input then Free Nuber used
            auxillary: bool, optional
                trigger if case is to be auxillary
            kmatrix: bool, optional
                trigger MatrixUpdateAfterEachIteration option
            pdelta: bool, optional
                trigger p-delta
            label: str, optional
                label for the loadcase, if not specified then same as number
        """
        # Collect existing cases in the model
        all_cases = self._structure.Cases.GetAll()
        existing_names = []
        existing_numbers = []
        for i in range(1, all_cases.Count + 1):
            lcase = self._rbt.IRobotCase(all_cases.Get(i))
            existing_names.append(lcase.Name)
            existing_numbers.append(lcase.Number)

        if name not in existing_names or number not in existing_numbers:
            case = self._structure.Cases.CreateSimple(
                number, name, nature, analize_type
            )
            if label is None or len(label) <= 0:
                case.label = str(number)
            else:
                case.label = label
            if auxillary:
                case.IsAuxillary = True
            if kmatrix or pdelta:
                params = self._rbt.IRobotNonlinearAnalysisParams(
                    case.GetAnalysisParams()
                )
            if kmatrix:
                params.MatrixUpdateAfterEachIteration = True
                case.SetAnalysisParams(params)
            if pdelta:
                params.PDelta = True
                case.SetAnalysisParams(params)
        else:
            print(f"Case {name} already exists.")

    def clear(self) -> None:
        """Clears all loadcases in the model"""
        case_selection = self._structure.Selections.CreatePredefined(
            self._rbt.IRobotPredefinedSelection.I_PS_CASE_SIMPLE_CASES
        )
        self._cases.DeleteMany(case_selection)
