from pathlib import Path
from typing import Any
from .._base import _BaseEditor
from ._latex import CASE_NATURE_MAP, escape


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

    def get_simple_loadcase(self, case_index: int = None, number: int = None) -> Any:
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

    def to_latex(
        self,
        path: str,
        caption: str = "Load Cases",
        label: str = "tab:loadcases",
    ) -> None:
        """Export simple load cases to a LaTeX table file.

        Parameters
        ----------
        path : str
            File path for the output .tex file.
        caption : str, optional
            Table caption. Defaults to "Load Cases".
        label : str, optional
            LaTeX label for cross-referencing. Defaults to "tab:loadcases".
        """
        all_cases = self.get_all_load_cases()
        rows: list[tuple[int, str, str]] = []
        for i in range(1, all_cases.Count + 1):
            lcase = self._rbt.IRobotCase(all_cases.Get(i))
            if int(lcase.Type) != 0:
                continue
            nature_str = CASE_NATURE_MAP.get(int(lcase.Nature), str(int(lcase.Nature)))
            rows.append((lcase.Number, lcase.Name, nature_str))

        lines = [
            r"\begin{table}[h]",
            r"\centering",
            rf"\caption{{{escape(caption)}}}",
            rf"\label{{{label}}}",
            r"\begin{tabular}{rll}",
            r"\hline",
            r"\textbf{No.} & \textbf{Name} & \textbf{Type} \\",
            r"\hline",
        ]
        for number, name, nature in rows:
            lines.append(rf"{number} & {escape(name)} & {escape(nature)} \\")
        lines += [
            r"\hline",
            r"\end{tabular}",
            r"\end{table}",
        ]

        p = Path(path)
        if p.is_dir():
            p = p / "loadcases.tex"
        p.write_text("\n".join(lines), encoding="utf-8")
