import math
from typing import Any
from .._base import _BaseEditor


class ViewManager(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._project = self._raw.Project

    def get_current_view(self) -> Any:
        """Returns current IRobotView object"""
        return self._rbt.IRobotView3(self._project.ViewMngr.GetView(1))

    def manipulate(
        self,
        zoom_factor: float | Any = None,
        rotation_x: float | Any = None,
        rotation_y: float | Any = None,
        rotation_z: float | Any = None,
        pan_up: float = 0.0,
        pan_right: float = 0.0,
        window_width: float | Any = None,
        window_height: float | Any = None,
    ) -> None:
        """
        Manipulates view zoom, rotation and size. This function is not perfect,
        requires a lot of iterations to achieve desired results.

        Parameters
        ----------
        zoom_factor: float
            Zoom factor, while more than 1 means zoom is closer to structure, and less, zoom is farther from structure.
        rotation_x: float
            Rotation in degrees around x axis.
        rotation_y: float
            Rotation in degrees around y axis.
        rotation_z: float
            Rotation in degrees around z axis.
        pan_up: float
            Pans up the view
        pan_right: float
            Pans right the view
        window_width: float
            Width of the window in mm
        window_height: float
            Height of the window in mm

        """

        view = self.get_current_view()
        if zoom_factor is not None:
            # TODO: This code is not ideal, can be improved to make sure view is always centered?
            left, top, right, bottom = view.GetZoom()
            # Calculate center of the zoom
            average_x = (left + right) / 2
            average_y = (top + bottom) / 2
            zoom_horizontal = abs(left - average_x) / zoom_factor

            zoom_vertical = abs(top - average_y) / zoom_factor
            view.SetZoom(
                average_x + zoom_horizontal - pan_right,
                average_y + zoom_vertical - pan_up,
                average_x - zoom_horizontal + pan_right,
                average_y - zoom_vertical + pan_up,
            )
            view.Redraw(0)

        if rotation_x is not None:
            # this will work only if view is rotated already (3D)
            view.Rotate(
                self._rbt.IRobotGeoCoordinateAxis.I_GCA_OX,
                rotation_x * math.pi / 180,
            )
        if rotation_y is not None:
            view.Rotate(
                self._rbt.IRobotGeoCoordinateAxis.I_GCA_OY,
                rotation_x * math.pi / 180,
            )
        if rotation_z is not None:
            view.Rotate(
                self._rbt.IRobotGeoCoordinateAxis.I_GCA_OZ,
                rotation_x * math.pi / 180,
            )
        if window_width and window_height is not None:
            view.SetSize(window_width, window_height)
        view.Redraw(0)

    def _set_display_cases(self, view: Any, cases: str) -> None:
        """Set which load cases are active for display.

        Parameters
        ----------
        cases: str
            'Simple Cases' — all simple load cases (predefined selection).
            'Combinations' — all load combinations (predefined selection).
            'all' — all cases and combinations.
            '<numbers>' — space-separated case numbers, e.g. '1 2 3'.
        """
        structure = self._raw.Project.Structure
        case_sel = view.Selection.Get(self._rbt.IRobotObjectType.I_OT_CASE)
        if cases == "Simple Cases":
            predefined = structure.Selections.CreatePredefined(
                self._rbt.IRobotPredefinedSelection.I_PS_CASE_SIMPLE_CASES
            )
            case_sel.FromText(predefined.ToText())
        elif cases == "Combinations":
            predefined = structure.Selections.CreatePredefined(
                self._rbt.IRobotPredefinedSelection.I_PS_CASE_COMBINATIONS
            )
            case_sel.FromText(predefined.ToText())
        elif cases == "all":
            case_sel.FromText("all")
        else:
            case_sel.FromText(cases)

    # Display
    def display(
        self,
        node_numbers: bool | None = None,
        bar_numbers: bool | None = None,
        section_shapes: bool | None = None,
        panel_interiors: bool | None = None,
        dimension_lines: bool | None = None,
        offsets: bool | None = None,
        supports: bool | None = None,
        releases: bool | None = None,
        with_codes: bool = False,
        panel_colors: bool | None = None,
        section_colors: bool | None = None,
        member_lcs: bool | None = None,
        panel_lcs: bool | None = None,
    ) -> None:
        """Function controls what is displayed in the view.
        There are many parameters in the API documentation I.2.12. not all are added here.

        Parameters
        ----------
        nodes_numbers: bool
            Trigger node numbers display
        bar_numbers: bool
            Trigger bar numbers display
        section_shapes: bool
            Section shapes display
        panel_interiors: bool
            Panel interiors display
        dimension_lines: bool
            Dimension lines display
        offsets: bool
            Offsets display
        supports: bool
            Supports display
        releases: bool
            Supports display
        with_codes:bool
            Codes display for supports or releases
        panel_colors: bool
            Panel colors display
        section_colors:
            Section colors display
        member_lcs:
            Member local coordinate system display
        panel_lcs:
            Panel local coordinate system display
        """
        view = self.get_current_view()
        if node_numbers is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_NODE_NUMBERS,
                node_numbers,
            )
        if bar_numbers is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_BAR_NUMBERS,
                bar_numbers,
            )
        if section_shapes is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_SECTIONS_SHAPE,
                section_shapes,
            )
        if panel_interiors is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_FE_PANEL_INTERIOR,
                panel_interiors,
            )
        if dimension_lines is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_OTHER_DIMENSION_LINES,
                dimension_lines,
            )
        if offsets is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_ADVANCED_OFFSETS,
                offsets,
            )
        if supports is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_SUPPORT_SYMBOLS,
                supports,
            )
            if with_codes:
                view.ParamsDisplay.Set(
                    self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_SUPPORT_CODES,
                    with_codes,
                )
        if releases is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_ADVANCED_RELEASE_SYMBOLS,
                releases,
            )
            if with_codes:
                view.ParamsDisplay.Set(
                    self._rbt.IRobotViewDisplayAttributes.I_VDA_ADVANCED_RELEASE_CODES,
                    with_codes,
                )
        if panel_colors is not None:  # Not sure about it
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_FE_COLOR_LEGEND,
                panel_colors,
            )
        if section_colors is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_FE_COLOR_LEGEND,
                section_colors,
            )
        if member_lcs is not None:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_LOCAL_SYSTEM_BARS,
                member_lcs,
            )
        if panel_lcs is not None:  # Does it cover both cladding and shell panels?
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_STRUCTURE_LOCAL_SYSTEM_PANELS,
                panel_lcs,
            )

        view.Redraw(0)

    def loads_display(
        self,
        display: bool = True,
        symbols: bool = False,
        values: bool = False,
        symbol_size: int | Any = None,
        cases: str = "Simple Cases",
    ) -> None:
        """Function controls if loads are to be displayed in the view.

        Parameters
        ----------
        display: bool, optional, default=True
            If False, all load symbols and values are hidden regardless of other parameters.
        symbols: bool
            Load symbols display
        values: bool
            Load values display
        symbol size: int
            Symbol size in range 1 to 10.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.

        """
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if not display:
            VDA = self._rbt.IRobotViewDisplayAttributes
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_SYMBOLS_CONCENTRATED, False)
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_SYMBOLS_LINEAR, False)
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_SYMBOLS_PLANAR, False)
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_SYMBOLS_UNIFORM_SIZE, False)
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_AUTOMATICALLY, False)
            view.ParamsDisplay.Set(VDA.I_VDA_LOADS_VALUES, False)
            view.Redraw(0)
            return
        if symbols:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_SYMBOLS_CONCENTRATED,
                True,
            )
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_SYMBOLS_LINEAR,
                True,
            )
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_SYMBOLS_PLANAR,
                True,
            )
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_SYMBOLS_UNIFORM_SIZE,
                True,
            )
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_AUTOMATICALLY,
                True,
            )
        if values:
            view.ParamsDisplay.Set(
                self._rbt.IRobotViewDisplayAttributes.I_VDA_LOADS_VALUES,
                True,
            )
        if symbol_size is not None:
            if symbol_size < 1:
                symbol_size = 1
            if symbol_size > 10:
                symbol_size = 10
            view.ParamsDisplay.SymbolSize = symbol_size
        view.Redraw(0)

    # Display displacements
    def display_displacements(
        self,
        display: bool = False,
        labels: bool = True,
        scale: int = 1,
        exact: bool = False,
        cases: str = "Simple Cases",
    ) -> None:
        """
        Displays deflection.

        Parameters
        ----------
        display: bool
            Trigger to display deflection.
        labels: bool
            Trigger to display labels.
        scale: int
            Rescale the labels.
        exact: bool
            Trigger exact deformation for rebars.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        # make this to work with shell and members
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if display:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_DEFORMATION_DEFORMATION,
                True,
            )
            if exact:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_DEFORMATION_EXACT,
                    True,
                )
            if labels:
                view.ParamsDiagram.Descriptions = (
                    self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
                )
            # if scale is not None:
            #     self._rbt.ParamsDiagram.SetScale(abs(scale))
        else:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_DEFORMATION_DEFORMATION,
                False,
            )
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_DEFORMATION_EXACT,
                False,
            )
        view.Redraw(0)

    # Display bar internal forces
    def display_member_forces(
        self,
        display: bool = True,
        Fx: bool = False,
        Fy: bool = False,
        Fz: bool = False,
        Mx: bool = False,
        My: bool = False,
        Mz: bool = False,
        labels: bool = True,
        scale: int | Any = None,
        filling: bool = False,
        pos_neg: bool = False,
        values_type: str = "all",
        cases: str = "Simple Cases",
    ) -> None:
        """
        Displays member forces as diagram or map.

        Parameters
        ----------
        display: bool, optional, default=True
            If False, all member force diagrams are hidden regardless of other parameters.
        Fx: bool
            Trigger Fx forces display.
        Fy: bool
            Trigger Fy forces display.
        Fz: bool
            Trigger Fz forces display.
        Mx: bool
            Trigger Mx forces display.
        My: bool
            Trigger My forces display.
        Mz: bool
            Trigger Mz forces display.
        labels: bool, optional
            Trigger to display labels.
        scale: int, optional
            Rescale the labels.
        filling: bool, optional
            Filling of the diagram.
        pos_neg: bool, optional
            Positive-negative differentiated.
        values_type: str, optional, default='all'
            Change display type of the values, possible: "global extremes", "all", "local extremes"
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        possible_values = ("all", "global extremes", "local extremes")
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if not display:
            VDRT = self._rbt.IRobotViewDiagramResultType
            for res_type in (
                VDRT.I_VDRT_NTM_FX,
                VDRT.I_VDRT_NTM_FY,
                VDRT.I_VDRT_NTM_FZ,
                VDRT.I_VDRT_NTM_MX,
                VDRT.I_VDRT_NTM_MY,
                VDRT.I_VDRT_NTM_MZ,
            ):
                view.ParamsDiagram.Set(res_type, False)
            view.Redraw(0)
            return
        if Fx:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_FX,
                True,
            )
        if Fy:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_FY,
                True,
            )
        if Fz:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_FZ,
                True,
            )
        if Mx:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_MX,
                True,
            )
        if My:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_MY,
                True,
            )
        if Mz:
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_NTM_MZ,
                True,
            )
        if labels:
            view.ParamsDiagram.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
            )
        # if scale is not None:
        #     self._rbt.ParamsDiagram.SetScale = abs(scale)

        if filling:
            view.ParamsDiagram.Filling = (
                self._rbt.IRobotViewDiagramFillingType.I_VDFT_FILLED
            )
        else:
            view.ParamsDiagram.Filling = (
                self._rbt.IRobotViewDiagramFillingType.I_VDFT_FENCE
            )

        if pos_neg:
            view.ParamsDiagram.PositiveNegative = (
                self._rbt.IRobotViewDiagramSignDifferType.I_VDSDT_DIFFERENTIATED
            )
        else:
            view.ParamsDiagram.PositiveNegative = (
                self._rbt.IRobotViewDiagramSignDifferType.I_VDSDT_UNDIFFERENTIATED
            )

        if values_type not in possible_values:
            raise ValueError(
                "Values type for member forces can by only: 'all', 'global extremes' or 'local extremes'."
            )
        else:
            view.ParamsDiagram.Values = self._rbt.IRobotViewDiagramValueType(
                possible_values.index(values_type)
            )
        view.Redraw(0)

    def display_utilisations(
        self,
        display: bool = True,
        labels: bool = True,
        text: bool = False,
        thickness_coeff: int = 5,
        cases: str = "Simple Cases",
    ) -> None:
        """Display utilisations of members in for of map on members.
        Make sure results from verification are available, otherwise this will fail.

        Parameters
        ----------
        display: bool
            Trigger to display deflection.
        labels: bool
            Trigger to display labels.
        text: bool
            Trigger to display text instead of labels. If True, then overwrites labels.
        thickness_coeff: int, optional, default=5
            Thickness map coefficient.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if display:
            view.ParamsBarMap.CurrentResult = (
                self._rbt.IRobotViewBarMapResultType.I_VBMRT_DESIGN_RATIO
            )
            view.ParamsBarMap.MapThicknessCoeff = thickness_coeff
        else:
            view.ParamsBarMap.CurrentResult = (
                self._rbt.IRobotViewBarMapResultType.I_VBMRT_NOTHING
            )
            view.Redraw(0)
            return
        if labels and text:
            labels = False
        if labels:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
            )
        elif text:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_TEXT
            )
        else:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_NONE
            )
        view.Redraw(0)

    def display_stresses(
        self,
        display: bool = True,
        s_max: bool = False,
        s_min: bool = False,
        mises: bool = False,
        labels: bool = False,
        text: bool = False,
        thickness_coeff: int = 5,
        cases: str = "Simple Cases",
    ) -> None:
        """
        Displays stressess on bar.

        Parameters
        ----------
        display: bool
            Trigger to display stresses.
        s_max: bool
            Display maximal stress
        s_min: bool
            Display minimal stress
        mises: bool
            Display von misses stress
        labels: bool
            Trigger to display labels.
        text: bool
            Trigger to display text instead of labels. If True, then overwrites labels.
        thickness_coeff: int, optional, default=5
            Thickness map coefficient.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """

        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if display:
            view.ParamsBarMap.MapThicknessCoeff = thickness_coeff
            if s_max:
                view.ParamsBarMap.CurrentResult = (
                    self._rbt.IRobotViewBarMapResultType.I_VBMRT_STRESS_S_MAX
                )
            elif s_min:
                view.ParamsBarMap.CurrentResult = (
                    self._rbt.IRobotViewBarMapResultType.I_VBMRT_STRESS_S_MIN
                )
            elif mises:
                view.ParamsFeMap.CurrentResult = (
                    self._rbt.IRobotViewFeMapResultType.I_VFMRT_COMPLEX_STRESSES
                )
        else:
            view.ParamsBarMap.CurrentResult = (
                self._rbt.IRobotViewBarMapResultType.I_VBMRT_NOTHING
            )
            view.Redraw(0)
            return

        if labels and text:
            labels = False
        if labels:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
            )
        elif text:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_TEXT
            )
        else:
            view.ParamsBarMap.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_NONE
            )
        view.Redraw(0)

    def display_member_stresses(
        self,
        display: bool = True,
        s_max: bool = False,
        s_min: bool = False,
        labels: bool = True,
        text: bool = False,
        cases: str = "Simple Cases",
    ) -> None:
        """
        Displays member stresses as diagrams along members via ParamsDiagram.

        Parameters
        ----------
        display: bool, optional, default=True
            If False, all member stress diagrams are hidden regardless of other parameters.
        s_max: bool
            Display maximum normal stress diagram.
        s_min: bool
            Display minimum normal stress diagram.
        labels: bool, optional, default=True
            Trigger to display labels.
        text: bool, optional, default=False
            Trigger to display text instead of labels. If True, overwrites labels.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        VDRT = self._rbt.IRobotViewDiagramResultType
        if not display:
            for res_type in (
                VDRT.I_VDRT_STRESS_S_MAX,
                VDRT.I_VDRT_STRESS_S_MIN,
            ):
                view.ParamsDiagram.Set(res_type, False)
            view.Redraw(0)
            return
        if s_max:
            view.ParamsDiagram.Set(VDRT.I_VDRT_STRESS_S_MAX, True)
        if s_min:
            view.ParamsDiagram.Set(VDRT.I_VDRT_STRESS_S_MIN, True)
        if labels and text:
            labels = False
        if labels:
            view.ParamsDiagram.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
            )
        elif text:
            view.ParamsDiagram.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_TEXT
            )
        else:
            view.ParamsDiagram.Descriptions = (
                self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_NONE
            )
        view.Redraw(0)

    def display_reactions(
        self,
        display: bool = True,
        Rx: bool = False,
        Ry: bool = False,
        Rz: bool = False,
        Mx: bool = False,
        My: bool = False,
        Mz: bool = False,
        local_system: bool = False,
        cases: str = "Simple Cases",
    ) -> None:
        """Display reactions

        Parameters
        ----------
        display: bool, optional, default=True
            If False, all reaction diagrams are hidden regardless of other parameters.
        Rx: bool
            Trigger Rx reaction display.
        Ry: bool
            Trigger Ry reaction display.
        Rz: bool
            Trigger Rz reaction display.
        Mx: bool
            Trigger Mx reaction display.
        My: bool
            Trigger My reaction display.
        Mz: bool
            Trigger Mz reaction display.
        local_system: bool, optional, default = False
            Trigger local system reactions display.
        cases: str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        if not display:
            VDRT = self._rbt.IRobotViewDiagramResultType
            for res_type in (
                VDRT.I_VDRT_REACTION_FORCES,
                VDRT.I_VDRT_REACTION_MOMENTS,
                VDRT.I_VDRT_REACTION_FX,
                VDRT.I_VDRT_REACTION_FY,
                VDRT.I_VDRT_REACTION_FZ,
                VDRT.I_VDRT_REACTION_MX,
                VDRT.I_VDRT_REACTION_MY,
                VDRT.I_VDRT_REACTION_MZ,
                VDRT.I_VDRT_REACTION_DESC,
            ):
                view.ParamsDiagram.Set(res_type, False)
            view.Redraw(0)
            return
        if any([Rx, Ry, Rz]):
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_FORCES,
                True,
            )
            if Rx:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_FX,
                    True,
                )
            if Ry:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_FY,
                    True,
                )
            if Rz:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_FZ,
                    True,
                )
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_DESC,
                True,
            )
        if any([Mx, My, Mz]):
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_MOMENTS,
                True,
            )
            if Mx:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_MX,
                    True,
                )
            if My:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_MY,
                    True,
                )
            if Mz:
                view.ParamsDiagram.Set(
                    self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_MZ,
                    True,
                )
            view.ParamsDiagram.Set(
                self._rbt.IRobotViewDiagramResultType.I_VDRT_REACTION_DESC,
                True,
            )
        if local_system:
            view.ParamsDiagram.ReactionsInLocalSystem = True
        else:
            view.ParamsDiagram.ReactionsInLocalSystem = False
        view.Redraw(0)

    def restore_default(self) -> None:
        """Apply a clean default view state.

        Resets every display attribute to a neutral
        starting point: structure visible, all result diagrams off, no load
        symbols, no annotations except support symbols.

        """
        view = self.get_current_view()
        pd = view.ParamsDisplay
        diag = view.ParamsDiagram
        bmap = view.ParamsBarMap
        VDA = self._rbt.IRobotViewDisplayAttributes
        VDRT = self._rbt.IRobotViewDiagramResultType

        # --- Structure annotations ---
        pd.Set(VDA.I_VDA_STRUCTURE_NODE_NUMBERS, False)
        pd.Set(VDA.I_VDA_STRUCTURE_BAR_NUMBERS, False)
        pd.Set(VDA.I_VDA_SECTIONS_SHAPE, False)
        pd.Set(VDA.I_VDA_FE_PANEL_INTERIOR, True)
        pd.Set(VDA.I_VDA_OTHER_DIMENSION_LINES, False)
        pd.Set(VDA.I_VDA_ADVANCED_OFFSETS, False)
        pd.Set(VDA.I_VDA_STRUCTURE_SUPPORT_SYMBOLS, True)
        pd.Set(VDA.I_VDA_STRUCTURE_SUPPORT_CODES, False)
        pd.Set(VDA.I_VDA_ADVANCED_RELEASE_SYMBOLS, False)
        pd.Set(VDA.I_VDA_ADVANCED_RELEASE_CODES, False)
        pd.Set(VDA.I_VDA_FE_COLOR_LEGEND, False)
        pd.Set(VDA.I_VDA_STRUCTURE_LOCAL_SYSTEM_BARS, False)
        pd.Set(VDA.I_VDA_STRUCTURE_LOCAL_SYSTEM_PANELS, False)

        # --- Load symbols: all off ---
        pd.Set(VDA.I_VDA_LOADS_SYMBOLS_CONCENTRATED, False)
        pd.Set(VDA.I_VDA_LOADS_SYMBOLS_LINEAR, False)
        pd.Set(VDA.I_VDA_LOADS_SYMBOLS_PLANAR, False)
        pd.Set(VDA.I_VDA_LOADS_SYMBOLS_UNIFORM_SIZE, False)
        pd.Set(VDA.I_VDA_LOADS_AUTOMATICALLY, False)
        pd.Set(VDA.I_VDA_LOADS_VALUES, False)

        # --- Display style ---
        pd.HiddenLines = self._rbt.IRobotViewHiddenLinesDisplayType.I_VHLDT_NONE
        pd.SymbolSize = 3

        # --- Diagram result types: all off ---
        for res_type in (
            VDRT.I_VDRT_NTM_FX,
            VDRT.I_VDRT_NTM_FY,
            VDRT.I_VDRT_NTM_FZ,
            VDRT.I_VDRT_NTM_MX,
            VDRT.I_VDRT_NTM_MY,
            VDRT.I_VDRT_NTM_MZ,
            VDRT.I_VDRT_DEFORMATION_DEFORMATION,
            VDRT.I_VDRT_DEFORMATION_EXACT,
            VDRT.I_VDRT_REACTION_FORCES,
            VDRT.I_VDRT_REACTION_MOMENTS,
            VDRT.I_VDRT_REACTION_FX,
            VDRT.I_VDRT_REACTION_FY,
            VDRT.I_VDRT_REACTION_FZ,
            VDRT.I_VDRT_REACTION_MX,
            VDRT.I_VDRT_REACTION_MY,
            VDRT.I_VDRT_REACTION_MZ,
            VDRT.I_VDRT_REACTION_DESC,
        ):
            diag.Set(res_type, False)

        # --- Diagram style ---
        diag.Descriptions = self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_LABELS
        diag.Filling = self._rbt.IRobotViewDiagramFillingType.I_VDFT_FENCE
        diag.PositiveNegative = (
            self._rbt.IRobotViewDiagramSignDifferType.I_VDSDT_UNDIFFERENTIATED
        )
        diag.ReactionsInLocalSystem = False

        # --- Bar map: off ---
        bmap.CurrentResult = self._rbt.IRobotViewBarMapResultType.I_VBMRT_NOTHING
        bmap.Descriptions = self._rbt.IRobotViewDiagramDescriptionType.I_VDDT_NONE
        bmap.MapThicknessCoeff = 5.0

        view.Redraw(0)

    def clear_results(self) -> None:
        """Hide all results currently displayed in the view.

        Turns off member force diagrams, deformation diagrams, reaction diagrams,
        member map results (utilisations, stresses), and shell/FE map results.
        Structure display settings (node numbers, supports, etc.) are not affected.
        """
        view = self.get_current_view()
        diag = view.ParamsDiagram
        VDRT = self._rbt.IRobotViewDiagramResultType

        for res_type in (
            VDRT.I_VDRT_NTM_FX,
            VDRT.I_VDRT_NTM_FY,
            VDRT.I_VDRT_NTM_FZ,
            VDRT.I_VDRT_NTM_MX,
            VDRT.I_VDRT_NTM_MY,
            VDRT.I_VDRT_NTM_MZ,
            VDRT.I_VDRT_DEFORMATION_DEFORMATION,
            VDRT.I_VDRT_DEFORMATION_EXACT,
            VDRT.I_VDRT_REACTION_FORCES,
            VDRT.I_VDRT_REACTION_MOMENTS,
            VDRT.I_VDRT_REACTION_FX,
            VDRT.I_VDRT_REACTION_FY,
            VDRT.I_VDRT_REACTION_FZ,
            VDRT.I_VDRT_REACTION_MX,
            VDRT.I_VDRT_REACTION_MY,
            VDRT.I_VDRT_REACTION_MZ,
            VDRT.I_VDRT_REACTION_DESC,
        ):
            diag.Set(res_type, False)

        view.ParamsBarMap.CurrentResult = (
            self._rbt.IRobotViewBarMapResultType.I_VBMRT_NOTHING
        )
        view.ParamsFeMap.CurrentResult = (
            self._rbt.IRobotViewFeMapResultType(
                -1, True
            )  # might be required to change to numeric value -1
        )
        view.Redraw(0)

    def display_shell_forces(self, Mxx, Myy, Mxy, Qxx, Qyy, results_lcs=0) -> None:
        pass

    def display_reinforcement_results(
        self,
        display: bool = True,
        Ax_neg: bool = False,
        Ax_pos: bool = False,
        Ay_neg: bool = False,
        Ay_pos: bool = False,
        deflection: bool = False,
        crack_x_neg: bool = False,
        crack_x_pos: bool = False,
        crack_y_neg: bool = False,
        crack_y_pos: bool = False,
        cases: str = "Simple Cases",
    ) -> None:
        """Display reinforcement results for shell/FE panels as a map.

        Only one result type can be active at a time. When multiple flags are
        ``True``, the first matching one in the order listed below is applied.
        Reinforcement area results use ``IRobotViewFeMapResultType``; cracking
        and deflection results use ``IRobotViewReinforcementResultType``.

        Priority order: Ax_neg → Ax_pos → Ay_neg → Ay_pos → deflection →
        crack_x_neg → crack_x_pos → crack_y_neg → crack_y_pos.

        Parameters
        ----------
        display : bool, optional, default=True
            If False, hides all FE map results regardless of other parameters.
        Ax_neg : bool, optional, default=False
            Display bottom (negative face) reinforcement area in the X direction
            (``I_VFMRT_COMPLEX_REINFORCE_BOTTOM_MXX``).
        Ax_pos : bool, optional, default=False
            Display top (positive face) reinforcement area in the X direction
            (``I_VFMRT_COMPLEX_REINFORCE_TOP_MXX``).
        Ay_neg : bool, optional, default=False
            Display bottom (negative face) reinforcement area in the Y direction
            (``I_VFMRT_COMPLEX_REINFORCE_BOTTOM_MYY``).
        Ay_pos : bool, optional, default=False
            Display top (positive face) reinforcement area in the Y direction
            (``I_VFMRT_COMPLEX_REINFORCE_TOP_MYY``).
        deflection : bool, optional, default=False
            Display deflection values (``I_VRRT_F``).
        crack_x_neg : bool, optional, default=False
            Display crack width on the bottom (negative) face in the X direction
            (``I_VRRT_AX``).
        crack_x_pos : bool, optional, default=False
            Display crack width on the top (positive) face in the X direction
            (``I_VRRT_AX``).
        crack_y_neg : bool, optional, default=False
            Display crack width on the bottom (negative) face in the Y direction
            (``I_VRRT_AY``).
        crack_y_pos : bool, optional, default=False
            Display crack width on the top (positive) face in the Y direction
            (``I_VRRT_AY``).
        cases : str, optional, default='Simple Cases'
            Cases to display. Accepts 'Simple Cases', 'Combinations', 'all',
            or space-separated case numbers e.g. '1 2 3'.
        """
        view = self.get_current_view()
        self._set_display_cases(view, cases)
        VFMRT = self._rbt.IRobotViewFeMapResultType
        VRRT = self._rbt.IRobotViewReinforcementResultType

        if not display:
            view.ParamsFeMap.CurrentResult = VFMRT(-1, True)
            view.Redraw(0)
            return

        if Ax_neg:
            view.ParamsFeMap.CurrentResult = VFMRT.I_VFMRT_COMPLEX_REINFORCE_BOTTOM_MXX
        elif Ax_pos:
            view.ParamsFeMap.CurrentResult = VFMRT.I_VFMRT_COMPLEX_REINFORCE_TOP_MXX
        elif Ay_neg:
            view.ParamsFeMap.CurrentResult = VFMRT.I_VFMRT_COMPLEX_REINFORCE_BOTTOM_MYY
        elif Ay_pos:
            view.ParamsFeMap.CurrentResult = VFMRT.I_VFMRT_COMPLEX_REINFORCE_TOP_MYY
        elif deflection:
            view.ParamsFeMap.CurrentResult = VRRT.I_VRRT_F
        elif crack_x_neg:
            view.ParamsFeMap.CurrentResult = VRRT.I_VRRT_AX
        elif crack_x_pos:
            view.ParamsFeMap.CurrentResult = VRRT.I_VRRT_AX
        elif crack_y_neg:
            view.ParamsFeMap.CurrentResult = VRRT.I_VRRT_AY
        elif crack_y_pos:
            view.ParamsFeMap.CurrentResult = VRRT.I_VRRT_AY

        view.Redraw(0)
