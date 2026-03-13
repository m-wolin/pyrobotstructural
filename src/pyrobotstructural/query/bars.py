from typing import Any
from .._base import _BaseEditor
from ..enums import LabelType


class BarsQuery(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def get_all(self) -> Any:
        """
        Gets all nodes in the Roboit Model.

        Returns
        ----------
            IRobotBarsServer: Server that manages bars defined in stucture
        """
        return self.structure.Bars.GetAll()

    def get_bar(self, bar_number: int, include_superbars=False) -> Any:
        """
        Returns the bar of given number.

        Parameters
        ----------
        bar_number: int
            index of a bar

        Returns
        ----------
            IRobotDataObject: bar object IRobotBar
        """
        bar_server = self.get_all()
        bar = self._rbt.IRobotBar(bar_server.Get(bar_number))
        if bar.IsSuperBar and not include_superbars:
            return None
        else:
            return bar

    def get_bar_section_data(self, bar: Any) -> Any:
        """
        Returns the bar section data.

        Parameters
        ----------
            bar: IRobotBar

        Returns
        ----------
            section label data (IRobotBarSectionData))
        """
        # nonstd_data = None
        section_label_data = self._rbt.IRobotBarSectionData(
            bar.GetLabel(LabelType.BAR_SECTION).Data
        )
        return section_label_data

    def get_all_bars_node_numbers(self) -> list:
        """
        Returns
        ----------
             All bar data in a list [bar_number, start_node_nr, end_node_nr].
        """
        bar_data = []
        all_bars = self.get_all()
        for i in range(1, all_bars.Count + 1):
            bar = self.get_bar(i)
            bar_data.append([bar.Number, bar.StartNode, bar.EndNode])
        return bar_data
