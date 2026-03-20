from pathlib import Path
from typing import Any
from .._base import _BaseEditor
from ._latex import COMB_TYPE_MAP, escape, format_factors


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
                    comb_type = COMB_TYPE_MAP.get(
                        int(lcomb.CombinationType), str(int(lcomb.CombinationType))
                    )
                    # TODO: add factors to the returned values
                    lcombs.append([name, number, comb_type])
        return lcombs

    def get_combination_factors(self, lcomb: Any) -> list[tuple[int, float]]:
        """Returns list of (case_number, factor) pairs for a combination.

        Parameters
        ----------
        lcomb : IRobotCaseCombination
            Combination object returned by get_all or get_single.

        Returns
        ----------
        list[tuple[int, float]]
        """
        case_factors = lcomb.CaseFactors
        return [
            (case_factors.Get(i).CaseNumber, case_factors.Get(i).Factor)
            for i in range(1, case_factors.Count + 1)
        ]

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

    def to_latex(
        self,
        path: str,
        caption: str = "Load Combinations",
        label: str = "tab:combinations",
    ) -> None:
        """Export load combinations to a LaTeX table file.

        Parameters
        ----------
        path : str
            File path for the output .tex file.
        caption : str, optional
            Table caption. Defaults to "Load Combinations".
        label : str, optional
            LaTeX label for cross-referencing. Defaults to "tab:combinations".
        """
        all_cases = self._structure.Cases.GetAll()
        rows: list[tuple[int, str, str, str]] = []
        for i in range(1, all_cases.Count + 1):
            lcase = self._rbt.IRobotCase(all_cases.Get(i))
            if int(lcase.Type) != 1:
                continue
            lcomb = self._rbt.IRobotCaseCombination(lcase)
            comb_type = COMB_TYPE_MAP.get(
                int(lcomb.CombinationType), str(int(lcomb.CombinationType))
            )
            factors_str = format_factors(lcomb.CaseFactors)
            rows.append((lcomb.Number, lcomb.Name, comb_type, factors_str))

        lines = [
            r"\begin{table}[h]",
            r"\centering",
            rf"\caption{{{escape(caption)}}}",
            rf"\label{{{label}}}",
            r"\begin{tabular}{rlll}",
            r"\hline",
            r"\textbf{No.} & \textbf{Name} & \textbf{Type} & \textbf{Factors} \\",
            r"\hline",
        ]
        for number, name, comb_type, factors_str in rows:
            lines.append(
                rf"{number} & {escape(name)} & {escape(comb_type)} & {factors_str} \\"
            )
        lines += [
            r"\hline",
            r"\end{tabular}",
            r"\end{table}",
        ]

        p = Path(path)
        if p.is_dir():
            p = p / "combinations.tex"
        p.write_text("\n".join(lines), encoding="utf-8")
