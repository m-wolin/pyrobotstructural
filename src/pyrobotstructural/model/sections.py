"""This module is meant to provide creating sections capability, bars and slabs
in future also complex sections?"""

from typing import Any
from .._base import _BaseEditor
from ..enums import LabelType, SectionType, SectionShapeType


class SectionEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels

    def create_tube_section(
        self,
        name: str,
        diameter: float,
        thickness: float,
        material: str,
    ) -> None:
        """
        Creates custom tubular section.

        Parameters
        ----------
        name: str
            Name of the section.
        diameter: float
            Diameter in meters
        thickness: float
            Thickness in meters
        material: str
            Material name
        """
        label = self.labels.Create(LabelType.BAR_SECTION, name)
        data = self._raw.IRobotBarSectionData(label.Data)
        data.Type = SectionType.TUBE
        data.ShapeType = SectionShapeType.TUBE
        nonstd_data = data.CreateNonstd(0.0)
        nonstd_data.SetValue(
            self._raw.IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D, diameter
        )  # I_BSDV_D
        nonstd_data.SetValue(
            self._raw.IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T, thickness
        )  # I_BSDV_TF
        data.CalcNonstdGeometry()
        data.MaterialName = material
        self.labels.Store(label)

    def create_rect_section(
        self, name: str, height: float, width: float, material: str
    ) -> None:
        """
        Creates custom solid rectangle section.

        Parameters
        ----------
        name: str
            Name of the section.
        height: float
            Height in meters
        width: float
            Width in meters
        material: str
            Material name
        TODO: Add option to create rectangle tube, so not filled
        """
        label = self.labels.Create(LabelType.BAR_SECTION, name)
        data = self._raw.IRobotBarSectionData(label.Data)
        data.Type = SectionType.RECT
        data.ShapeType = SectionShapeType.RECT_FILLED
        nonstd_data = data.CreateNonstd(0.0)
        nonstd_data.SetValue(
            self._raw.IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B, width / 1000
        )  # I_BSNDV_RECT_B
        nonstd_data.SetValue(
            self._raw.IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H, height / 1000
        )  # I_BSNDV_RECT_H
        data.CalcNonstdGeometry()
        data.MaterialName = material
        self.labels.Store(label)

    def apply_section_to_bar(self, bar_number: int, section_name: str) -> None:
        """
        Applies section to a existing bar.

        Parameters
        ----------
        bar_number: int
            Bar number
        section_name: str,
            Section name, assume it exists

        """
        bar = self._raw.IRobotBar(self.structure.Bars.Get(bar_number))
        bar.SetLabel(LabelType.BAR_SECTION, section_name)

    # TODO: load section from database
