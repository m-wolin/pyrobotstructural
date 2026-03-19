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
        data = self._rbt.IRobotBarSectionData(label.Data)
        data.Type = SectionType.TUBE
        data.ShapeType = SectionShapeType.TUBE
        nonstd_data = data.CreateNonstd(0.0)
        nonstd_data.SetValue(
            self._rbt.IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D, diameter
        )  # I_BSDV_D
        nonstd_data.SetValue(
            self._rbt.IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T, thickness
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
        data = self._rbt.IRobotBarSectionData(label.Data)
        data.Type = SectionType.RECT
        data.ShapeType = SectionShapeType.RECT_FILLED
        nonstd_data = data.CreateNonstd(0.0)
        nonstd_data.SetValue(
            self._rbt.IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B, width / 1000
        )  # I_BSNDV_RECT_B
        nonstd_data.SetValue(
            self._rbt.IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H, height / 1000
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
        bar = self._rbt.IRobotBar(self.structure.Bars.Get(bar_number))
        bar.SetLabel(LabelType.BAR_SECTION, section_name)

    def load_from_database(self, database_name: str, section_name: str) -> None:
        """Loads a section from database. Database must be added into Robot manually first,
        depending on regional settings Robot contains some default bases, eg. EURO, EC5, RUSER

        Parameters
        ----------
        database_name: str
            Database name it must exist in Robot file
        section_name: str,
            Section name, assume it exists in given database
        """
        sdl = self._raw.Project.Preferences.SectionsActive
        base_index = sdl.Find(database_name)
        if base_index > 0:
            database = sdl.GetDatabase(base_index)
            sections = database.GetAll()
            if sections.Find(section_name, 1):
                section_label = self._labels.Create(LabelType.BAR_SECTION, section_name)
                section_data = self._rbt.IRobotBarSectionData(section_label.Data)
                section_data.LoadFromDBase(section_name)
                self._labels.Store(section_label)
                print(f"Section {section_name} loaded from {database_name} database.")
            else:
                print(f"Section {section_name} not found in the database!")
                raise ValueError
        else:
            print(f"Database {database_name} not found!")
            raise ValueError

    def add_database(self, database_name: str) -> None:
        """Adds database of given name to the Robot project.
        It must be one of the databases which exist in Robot files.
        Go to: Job Preferences -> Databases -> Steel and Timber Sections -> Add new

        Parameters
        ----------
        database_name: str
            Database name it must exist in Robot databases.
        """
        sdl = self._raw.Project.Preferences.SectionsActive
        sdl.Add(database_name)
