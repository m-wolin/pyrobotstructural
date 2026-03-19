from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Union
from .._base import _BaseEditor
from ..enums import LabelType, ThicknessType
import numpy as np


class GeometryEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._project = self._raw.Project
        self._structure = self._project.Structure
        self._labels = self._structure.Labels

    @contextmanager
    def begin_edit(self):
        """Context manager that batches all structure modifications into a
        single multi-operation flush, dramatically reducing COM overhead for
        large bulk operations.

        Usage
        -----
        with app.model.geometry.begin_edit():
            app.model.geometry.add_node([[1, 0, 0, 0], [2, 1, 0, 0]])
            app.model.geometry.add_member([[1, 1, 2]], section_name="IPE 100")
        """
        self._structure.BeginMultiOperation()
        try:
            yield
        finally:
            self._structure.EndMultiOperation()

    def add_node(
        self,
        number_or_data: Union[int, list, np.ndarray],
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
    ) -> None:
        """
        Add one or more nodes to the model.

        Parameters
        ----------
        number_or_data : int | list | np.ndarray
            - Single node: pass number (int) alongside x, y, z.
            - Multiple nodes: pass a 2D list or numpy array of shape (N, 4)
            where each row is [number, x, y, z].
        x, y, z : float, optional
            Coordinates in meters. Only used when adding a single node.

        Examples
        --------
        # Single node
        model.add_node(1, 0.0, 1.0, 2.0)

        # List of nodes
        model.add_node([[1, 0.0, 1.0, 2.0],
                        [2, 3.0, 4.0, 5.0]])

        # Numpy array
        nodes = np.array([[1, 0.0, 1.0, 2.0],
                        [2, 3.0, 4.0, 5.0]])

        model.add_node(nodes)
        """
        nodes = self._structure.Nodes

        # --- bulk input (list or numpy array) ---
        if isinstance(number_or_data, (list, np.ndarray)):
            data = np.asarray(number_or_data)

            if data.ndim != 2 or data.shape[1] != 4:
                raise ValueError(
                    "Bulk input must have shape (N, 4) — columns: [number, x, y, z]. "
                    f"Got shape {data.shape}."
                )

            self._structure.BeginMultiOperation()
            try:
                for row in data:
                    nodes.Create(int(row[0]), float(row[1]), float(row[2]), float(row[3]))
            finally:
                self._structure.EndMultiOperation()

        # --- single node ---
        elif isinstance(number_or_data, (int, np.integer)):
            if any(v is None for v in (x, y, z)):
                raise ValueError(
                    "x, y, and z must be provided when adding a single node."
                )
            nodes.Create(int(number_or_data), float(x), float(y), float(z))

        else:
            raise TypeError(
                f"Expected int, list, or np.ndarray for first argument, got {type(number_or_data).__name__}."
            )

    def add_member(
        self,
        number_or_data: Union[int, list, np.ndarray],
        start_node: int | None = None,
        end_node: int | None = None,
        section_name: Any | str = None,
        material_name: Any | str = None,
        release_name: Any | str = None,
        tension_comp: Any | str = None,
        truss: bool = False,
    ) -> None:
        """
        Add one or more bars to the model.

        Parameters
        ----------
        number_or_data : int | list | np.ndarray
            - Single bar: pass bar number (int) alongside start_node and end_node.
            - Multiple bars: pass a 2-D list or numpy array of shape (N, 3)
            where each row is [member_number, start_node, end_node].
        start_node : int, optional
            Start node number. Only used when adding a single bar.
        end_node : int, optional
            End node number. Only used when adding a single bar.
        section_name : str, optional
            Section name — must already exist in the model.
        material_name : str, optional
            Material name — must already exist in the model.
        release_name : str, optional
            Release name — must already exist in the model.
        tension_comp : str, optional
            'tension' for tension-only, 'compression' for compression-only.
        truss : bool, optional
            If True, sets the bar as a truss element (axial forces only).

        Examples
        --------
        # Single member
        model.add_member(1, 1, 2, section_name="HEA200")

        # Multiple members — list or numpy array
        model.add_member([[1, 1, 2],
                        [2, 2, 3],
                        [3, 3, 4]], section_name="HEA200")

        model.add_member(np.array([[1, 1, 2],
                                [2, 2, 3]]), truss=True)
        """
        # --- normalise input into a list of (number, start, end) tuples ---
        if isinstance(number_or_data, (int, np.integer)):
            if start_node is None or end_node is None:
                raise ValueError(
                    "start_node and end_node must be provided when adding a single member."
                )
            members = [(int(number_or_data), int(start_node), int(end_node))]

        elif isinstance(number_or_data, (list, np.ndarray)):
            data = np.asarray(number_or_data)
            if data.ndim != 2 or data.shape[1] != 3:
                raise ValueError(
                    "Bulk input must have shape (N, 3) — columns: "
                    f"[member_number, start_node, end_node]. Got shape {data.shape}."
                )
            members = [(int(row[0]), int(row[1]), int(row[2])) for row in data]

        else:
            raise TypeError(
                f"Expected int, list, or np.ndarray for first argument, "
                f"got {type(number_or_data).__name__}."
            )

        # --- create all bars, then apply shared labels ---
        self._structure.BeginMultiOperation()
        try:
            for number, start, end in members:
                self._structure.Bars.Create(number, start, end)
                bar = self._structure.Bars.Get(number)

                if section_name is not None:
                    bar.SetLabel(LabelType.BAR_SECTION, section_name)
                if material_name is not None:
                    bar.SetLabel(LabelType.MATERIAL, material_name)
                if release_name is not None:
                    bar.SetLabel(LabelType.BAR_RELEASE, release_name)
                if tension_comp is not None:
                    tc_value = 1 if tension_comp == "tension" else 2
                    bar.TensionCompression = self._raw.IRbotBarTensionCompression(tc_value)
                if truss:
                    bar.TrussBar = True
        finally:
            self._structure.EndMultiOperation()

    def add_contour(
        self,
        points: list[list[float, float, float]],
        number: Any | int = None,
    ) -> int:
        """
        Adds a contour object to the model.

        Parameters
        ----------
        points: list[list[float, float, float]]
            List of points, each point to be list of coordinates x, y, z
        number: Any|int, optional
            Number of the contour object, optional, if you specify number make sure it is free.

        Returns
        -------
        int
            Number of the created contour.
        """
        obj_server = self._structure.Objects

        # User can specify their number or free number will be used
        # TODO: Add a error check if specified number already exist in the model and raise error or use freenumber
        if number is not None:
            num = number
        else:
            num = obj_server.FreeNumber

        # Add points to the array
        points_array = self._rbt.IRobotPointsArray(
            self._raw.CmpntFactory.Create(
                self._rbt.IRobotComponentType.I_CT_POINTS_ARRAY
            )
        )

        points_array.SetSize(len(points))

        for point in points:
            points_array.Set(point[0], point[1], point[2], point[3])

        # Create contour
        obj_server.CreateContour(num, points_array)

        return num

    def add_cladding(
        self,
        points: list[list[float, float, float]],
        number: Any | int = None,
        load_distribution: str = "Two-way",
        # method: str = "trapezoidal",
    ) -> None:
        """
        Adds a cladding object to the model.

        Parameters
        ----------
        points: list[list[float, float, float]]
            List of points, each point to be list of coordinates x, y, z
        number: Any|int, optional
            Number of the contour object, optional, if you specify number make sure it is free.
        load_distribution: str, optional, default=two-way
            Load distribution settings, it can be either: 'Two-way', 'One-way X', 'One-way Y'.
        TODO: add option to provide local coordinate system
        """
        load_distributions = [
            "Two-way",
            "One-way X",
            "One-way Y",
        ]  # This is hardcoded. I am not sure if Robot allows to create custom types
        if load_distribution not in load_distributions:
            print("Wrong load distribution parameter in add_cladding function")
            raise ValueError
        num = self.add_contour(points=points, number=number)
        obj_server = self._structure.Objects
        contour = self._rbt.IRobotObjObject(obj_server.Get(num))
        contour.Main.Attribs.Meshed = False
        contour.SetLabel(LabelType.CLADDING, load_distribution)
        contour.Initialize()
        contour.Update()

    def add_shell_by_contour(
        self,
        points: list[list[float, float, float]],
        number: Any | int = None,
        material_name: Any | str = None,
        thickness: Any | float = None,
        thickness_name: Any | str = None,
    ) -> None:
        """
        Adds a shell panel object to the model.

        Parameters
        ----------
        points: list[list[float, float, float]]
            List of points, each point to be list of coordinates x, y, z
        number: Any|int, optional
            Number of the contour object, optional, if you specify number make sure it is free.
        matarial_name: str
            Material name
        thickness: float
            Thickness, curently only constant thickness is supported. Currently only homogeneous thickness supported.
        TODO: support variable thickness eg. thicknessData.Type = I_THT_VARIABLE_ALONG_LINE, thicknessData.Thick1,
        thicknessData.Thick2

        """
        if number is not None:
            contour_number = number
        else:
            contour_number = self._structure.Objects.FreeNumber
        num = self.add_contour(points=points, number=contour_number)

        # shell.Update
        if material_name is not None:
            if material_name is None:
                print("Thickness must be assigned!")
                raise ValueError
            if thickness is not None:
                # TODO: must check if thickness already exist if yes then skip definition part
                th_label = self._rbt.IRobotLabel(
                    self._structure.Labels.Create(
                        LabelType.PANEL_THICKNESS, thickness_name
                    )
                )
                thickness_ = self._rbt.IRobotThicknessData(th_label.Data)
                thickness_.MaterialName = material_name
                thickness_.ThicknessType = ThicknessType.HOMOGENEOUS
                th_data = self._rbt.IRobotThicknessHomoData(thickness_.Data)
                th_data.ThickConst = thickness
                self._labels.Store(th_label)
                # TODO: make below code working, if user specifies variable thickness along line
                # thicknessData.Type = I_THT_VARIABLE_ALONG_LINE
                # thicknessData.Thick1 = 0.1
                # thicknessData.Thick2 = 0.2
                # thicknessData.SetP1 = x,y,z
                # thicknessData.SetP2 = x,y,z
        else:
            print("Material name must be assigned!")
            raise ValueError
        shell = self._rbt.IRobotObjObject(self._structure.Objects.Get(num))
        shell.Main.Attribs.Meshed = True
        shell.SetLabel(LabelType.PANEL_THICKNESS, thickness_name)
        shell.Initialize()
