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
        self, symbols: bool = False, values: bool = False, symbol_size: int | Any = None
    ) -> None:
        """Function controls if loads are to be displayed in the view.

        Parameters
        ----------
        symbols: bool
            Load symbols display
        values: bool
            Load values display
        symbol size: int
            Symbol size in range 1 to 10.

        """
        view = self.get_current_view()
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

    # Display displacements
    def display_displacements(
        self,
        display: bool = False,
        labels: bool = True,
        scale: int = 1,
        exact: bool = False,
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
        """
        # make this to work with shell and members
        view = self.get_current_view()
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
            if scale is not None:
                self._rbt.ParamsDiagram.SetScale(abs(scale))

    # Display bar internal forces
    def display_member_forces(
        self,
        Fx: bool,
        Fy: bool,
        Fz: bool,
        Mx: bool,
        My: bool,
        Mz: bool,
        labels: bool = True,
        scale=None,
        filling=False,
        pos_neg=False,
        values_type="all",
    ) -> None:
        """
        Displays member forces as diagram or map.

        Parameters
        ----------
        Fx: bool
            Trigger Fx forces display.
        Fy: bool
            Trigger Fx forces display.
        Fz: bool
            Trigger Fx forces display.
        Mx: bool
            Trigger Fx forces display.
        My: bool
            Trigger Fx forces display.
        Mz: bool
            Trigger Fx forces display.
        labels: bool, optional
            Trigger to display labels.
        scale: int, optional
            Rescale the labels.
        filling: bool, optional
            Filling of the diagram.
        pos_neg: bool, optional
            Positive-negative differentiated.
        values_type: str, optional, default='global'
            Change display type of the values, possible: "global extremes", "all", "local extremes"
        """
        possible_values = ("all", "global extremes", "local extremes")
        view = self.get_current_view()
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
        if scale is not None:
            self._rbt.ParamsDiagram.SetScale(abs(scale))

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

    def display_utilisations(
        self,
        display: bool = True,
        labels: bool = True,
        text: bool = False,
        thickness_coeff: int = 5,
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
        """
        view = self.get_current_view()
        if display:
            view.ParamsBarMap.CurrentResult = (
                self._rbt.IRobotViewBarMapResultType.I_VBMRT_DESIGN_RATIO
            )
            view.ParamsBarMap.MapThicknessCoeff = thickness_coeff
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

    def display_stresses(
        self,
        display: bool = True,
        s_max: bool = False,
        s_min: bool = False,
        mises: bool = False,
        labels: bool = False,
        text: bool = False,
        thickness_coeff: int = 5,
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
        """

        view = self.get_current_view()
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

    def display_reactions(
        self,
        Rx: bool = False,
        Ry: bool = False,
        Rz: bool = False,
        Mx: bool = False,
        My: bool = False,
        Mz: bool = False,
        local_system: bool = False,
    ) -> None:
        # It might be required to use none and value, because once set to True, they will stay sitched on?
        """Display reactions

        Parameters
        ----------
        Fx: bool
            Trigger Fx reaction display.
        Fy: bool
            Trigger Fx reaction display.
        Fz: bool
            Trigger Fx reaction display.
        Mx: bool
            Trigger Fx reaction display.
        My: bool
            Trigger Fx reaction display.
        Mz: bool
            Trigger Fx reaction display.
        local_system: bool, optional, default = False
            Trigger local system reactions display.
        """
        view = self.get_current_view()
        if any(Rx, Ry, Rz):
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
        if any(Mx, My, Mz):
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

    def display_shell_forces(self, Mxx, Myy, Mxy, Qxx, Qyy, results_lcs=0) -> None:
        pass

    def display_reinforcement_results(
        self,
        Ax_neg,
        Ax_pos,
        Ay_neg,
        Ay_pos,
        deflection,
        crack_x_neg,
        crack_x_pos,
        crack_y_neg,
        crack_y_pos,
    ) -> None:
        pass
