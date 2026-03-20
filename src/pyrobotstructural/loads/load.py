from typing import Any
import math
from .._base import _BaseEditor


deg_to_rad = math.pi / 180


class LoadEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._cases = self._structure.Cases
        self._case_cache: dict[str, Any] = {}

    def add_self_weight(
        self, case_name: str, objects: int | str, factors: list = [0, 0, -1]
    ) -> None:
        """Adds self-weight to objects.

        Parameters
        ----------
            case_name: str
                Loadcase name to which the load will be asigned.
            objects: str
                List of objects eg. "1 2 3" or "all"
            factors: list
                Factors in format [x, y, z] sign factor is assumed as a direction for the factor
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(7))
        record = self._rbt.IRobotLoadRecord(case.Records.Get(record_index))
        load_factor_X = factors[0]
        load_factor_Y = factors[1]
        load_factor_Z = factors[2]
        if load_factor_X != 0:
            sign = math.copysign(1, load_factor_X)
            record.SetValue(0, sign)
            record.SetValue(3, abs(load_factor_X))
        elif load_factor_Y != 0:
            sign = math.copysign(1, load_factor_Y)
            record.SetValue(1, sign)
            record.SetValue(3, abs(load_factor_Y))
        elif load_factor_Z != 0:
            sign = math.copysign(1, load_factor_Z)
            record.SetValue(2, sign)
            record.SetValue(3, abs(load_factor_Z))
        if objects.lower() == "all":
            record.SetValue(15, 1)  # Ensure 'whole structure' setting
            record.Objects.FromText(str(objects))
        else:
            record.Objects.FromText(str(objects))

    def add_node_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        rotations: list = [0, 0, 0],
    ) -> None:
        """Adds point load on a node.

        Parameters
        ----------
            case_name: str
                Loadcase name to which the load will be asigned.
            objects: str
                List of objects eg. "1 2 3".
            loads: list
                Loads in format [Fx, Fy, Fz, Mx, My, Mz] in Newtons.
            rotations: list[float,float,float])
                Rotations angle in order: [alfa, beta, gamma] in degrees.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(0))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Fx
        record.SetValue(1, loads[1])  # Fy
        record.SetValue(2, loads[2])  # Fz
        record.SetValue(3, loads[3])  # Mx
        record.SetValue(4, loads[4])  # My
        record.SetValue(5, loads[5])  # Mz
        record.SetValue(8, rotations[0] * deg_to_rad)  # alfa
        record.SetValue(9, rotations[1] * deg_to_rad)  # beta
        record.SetValue(10, rotations[2] * deg_to_rad)  # gamma

    def add_uniform_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        dis_y: float = 0,
        dis_z: float = 0,
        projected: int = 0,
        rotations: list = [0, 0, 0],
        coord_sys: int = 0,
    ) -> None:
        """Adds uniform load on a member.

        Parameters
        ----------
        loads: list
            Loads in format [Fx, Fy, Fz, Mx, My, Mz] in Newtons/m
        case_name: str
            Loadcase name to which the load will be asigned.
        objects: str
            List of objects eg. "1 2 3"
        dis_y: float
            Eccentricity distance in y direction in local system
        dis_z: float
            Eccentricity distance in z direction in local system
        projected: int
            0 -not projected, 1-projected
        rotations: list[float,float,float]
            Rotations angle in order: [alfa, beta, gamma] in degrees.
        coord_sys: int
            0 - absolute, 1 - relative local system
        """
        case = self._get_case_by_name(case_name)
        if case is None:
            print(f"Case {case_name} does not exist!")
            raise ValueError
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(5))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Fx
        record.SetValue(1, loads[1])  # Fy
        record.SetValue(2, loads[2])  # Fz
        record.SetValue(3, loads[3])  # Mx
        record.SetValue(4, loads[4])  # My
        record.SetValue(5, loads[5])  # Mz
        record.SetValue(8, rotations[0] * deg_to_rad)  # alfa
        record.SetValue(9, rotations[1] * deg_to_rad)  # beta
        record.SetValue(10, rotations[2] * deg_to_rad)  # gamma
        record.SetValue(11, coord_sys)  # coordination system local/global
        record.SetValue(13, projected)  # projected
        record.SetValue(21, dis_y)  # dis_y
        record.SetValue(22, dis_z)  # diz_z

    def add_point_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        dis_x: float = 0,
        dis_y: float = 0,
        dis_z: float = 0,
        rotations: list = [0, 0, 0],
        coord_sys: int = 0,
        calc_node: int = 1,
        relabs: int = 0,
    ) -> None:
        """Adds point load on a member.

        Parameters
        ----------
            loads: list
                Loads in format [Fx, Fy, Fz, Mx, My, Mz] in Newtons
            case_name: str
                Loadcase name to which the load will be asigned.
            objects: str
                List of objects eg. "1 2 3"
            dis_x: float
                Load position from start node of the member.
            dis_y: float
                Eccentricity distance in y direction in local system.
            dis_z: float
                Eccentricity distance in z direction in local system.
            rotations: list[float,float,float]
                Rotations angle in order: [alfa, beta, gamma] in degrees.
            coord_sys: int
                0 - global, 1 - local system
            calc_node: int
                Create a calculation node in the load position, 0 - no node. Defaults to 1.
            relabs: int
                0 - absolute, 1 - relative. Distance values measured along bar length.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(3))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Fx
        record.SetValue(1, loads[1])  # Fy
        record.SetValue(2, loads[2])  # Fz
        record.SetValue(3, loads[3])  # Mx
        record.SetValue(4, loads[4])  # My
        record.SetValue(5, loads[5])  # Mz
        record.SetValue(8, rotations[0] * deg_to_rad)  # alfa
        record.SetValue(9, rotations[1] * deg_to_rad)  # beta
        record.SetValue(10, rotations[2] * deg_to_rad)  # gamma
        record.SetValue(11, coord_sys)  # coordination system local/global
        record.SetValue(12, calc_node)  # calcnode
        record.SetValue(13, relabs)  # relabs
        record.SetValue(6, dis_x)  # disX
        record.SetValue(21, dis_y)  # dis_y
        record.SetValue(22, dis_z)  # diz_z

    def add_trapezoidal_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        start_dist: float,
        end_dist: float,
        projected: int = 0,
        rotations: list = [0, 0, 0],
        coord_sys: int = 0,
    ) -> None:
        """Adds trapezoidal load (2p).

        Parameters
        ----------
            loads: list
                Loads in format [Px1, Py1, Pz1, Px2, Py2, Pz2] in kN/m
            case_name: str
                Loadcase name to which the load will be asigned
            objects: str
                List of objects eg. "1 2 3".
            start_dist: float
                Distance of the load starting point from bar origin.
            end_dist: float
                Distance of the load end point from bar origin.
            projected: int
                0 -not projected, 1-projected.
            rotations: list[float,float,float]
                Rotations angle in order: [alfa, beta, gamma] in degrees.
            coord_sys: int
                0 - absolute, 1 - relative. Distance values measured along bar length.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(6))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Px
        record.SetValue(1, loads[1])  # Py
        record.SetValue(2, loads[2])  # Pz
        record.SetValue(3, loads[3])  # Px2
        record.SetValue(4, loads[4])  # Py2
        record.SetValue(5, loads[5])  # Pz2
        record.SetValue(6, end_dist)  # disx2
        record.SetValue(7, start_dist)  # disx
        record.SetValue(8, rotations[0] * deg_to_rad)  # alfa
        record.SetValue(9, rotations[1] * deg_to_rad)  # beta
        record.SetValue(10, rotations[2] * deg_to_rad)  # gamma
        record.SetValue(12, projected)  # projected
        record.SetValue(13, coord_sys)  # coord system

    def add_uniform_panel_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        projected: int = 0,
        coord_sys: int = 0,
    ) -> None:
        """Adds uniform panel load.

        Parameters
        ----------
            loads: list
                Loads in format [Px, Py, Pz] in Pa
            case_name: str
                Loadcase name to which the load will be asigned.
            objects: str
                List of objects eg. "1 2 3".
            projected: int
                0 -not projected, 1-projected
            coord_sys: int
                0 - absolute, 1 - relative. Distance values measured along bar length.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(26))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Px
        record.SetValue(1, loads[1])  # Py
        record.SetValue(2, loads[2])  # Pz
        record.SetValue(11, coord_sys)  # cosystem
        record.SetValue(12, projected)  # projected

    def add_linear_load_on_edge(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        coord_sys: int,
        gamma: float,
    ) -> None:
        """Adds point load on a member

        Parameters
        ----------
            loads: list
                Loads in format [Fx, Fy, Fz, Mx, My, Mz] in Newtons
            case_name: str
                Loadcase name to which the load will be asigned
            objects: str
                List of objects eg. "1 2 3"
            coord_sys: int
                0 - global, 1 - local system
            gamma: float
                Gamma rotation angle in degrees. Defaults to 0.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(69))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Fx
        record.SetValue(1, loads[1])  # Fy
        record.SetValue(2, loads[2])  # Fz
        record.SetValue(3, loads[3])  # Mx
        record.SetValue(4, loads[4])  # My
        record.SetValue(5, loads[5])  # Mz
        record.SetValue(6, gamma * deg_to_rad)  # gamma
        record.SetValue(11, coord_sys)  # localsystem

    def add_contour_load(
        self,
        loads: list,
        case_name: str,
        contour_points: list,
        objects: str = None,
        load_3p: bool = False,
        p3_coordinates: list = None,
        auto_detect: bool = False,
        vector: tuple = None,
    ) -> None:
        """Adds load on contour.

        Parameters
        ----------
            loads: list
                Loads in format [Px, Py, Pz], if 3p load then [Px1, Py1, Pz1, Px2, Py2, Pz2, Px3, Py3, Pz3]
            case_name: str
                Loadcase name to which the load will be asigned
            contour_points: list
                Contour points in given format [[x,y,z], [x,y,z], ...]
            objects: str
                List of objects eg. "1 2 3"
            load_3p: bool, optional
                Triggers if load 3p on contour type is required.
            p3_coordinates: list, optional
                List of corner points for load 3p contour in format  [[x,y,z], [x,y,z], ...]
            auto_detect: bool, optional
                Trigger to auto detect panels for contour load distribution. Defaults to False.
            vector: tuple, optional
                Vector for force direction in format: (x,y,z). Defaults as downward (0,0,-1)
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(28))
        record = self._rbt.IRobotLoadRecordInContour(case.Records.Get(record_index))
        if auto_detect or objects is None:
            record.SetValue(-1, 1)
        else:
            record.Objects.FromText(objects)
        if vector is None:
            record.SetVector(0, 0, -1)  # vector downward
        else:
            record.SetValue(vector)
        # Assign contour loads
        if not load_3p:
            record.SetValue(0, loads[0])  # Px
            record.SetValue(1, loads[1])  # Py
            record.SetValue(2, loads[2])  # Pz
        else:
            record.SetValue(0, loads[0])  # Px1
            record.SetValue(1, loads[1])  # Py1
            record.SetValue(2, loads[2])  # Pz1
            record.SetValue(3, loads[3])  # Px2
            record.SetValue(4, loads[4])  # Py2
            record.SetValue(5, loads[5])  # Pz2
            record.SetValue(6, loads[6])  # Px3
            record.SetValue(7, loads[7])  # Py3
            record.SetValue(8, loads[8])  # Pz3
        # Assign contour points
        size = len(contour_points)
        record.SetValue(13, size)  # Assign size for point array I_ICRV_NPOINTS
        n = 1  # Order number for each contour point
        for point in contour_points:
            record.SetContourPoint(n, point[0], point[1], point[2])
            n += 1
        if load_3p:
            corner_number = 1  # Order number for coner point, it goes up to three.
            for lpoint in p3_coordinates:
                record.SetPoint(corner_number, lpoint[0], lpoint[1], lpoint[2])
                corner_number += 1

    def add_planar_3p_load(
        self,
        case_name: str,
        objects: int | str,
        loads: list,
        p1: list,
        p2: list,
        p3: list,
        projected: int = 0,
        coord_sys: int = 0,
    ) -> None:
        """Adds a planar 3-point (trapezoidal) load on panel/FE objects.

        The load intensity is defined at three reference points, allowing a
        linearly-varying distribution across the surface.

        Parameters
        ----------
        case_name : str
            Loadcase name to which the load will be assigned.
        objects : int | str
            Panel/FE object selection, e.g. ``"1 2 3"`` or a single int.
        loads : list
            Nine load components in order:
            ``[Px1, Py1, Pz1, Px2, Py2, Pz2, Px3, Py3, Pz3]`` in Pa.
        p1 : list
            Coordinates ``[x, y, z]`` of reference point 1 (in metres).
        p2 : list
            Coordinates ``[x, y, z]`` of reference point 2 (in metres).
        p3 : list
            Coordinates ``[x, y, z]`` of reference point 3 (in metres).
        projected : int, optional
            ``0`` – not projected, ``1`` – projected. Defaults to ``0``.
        coord_sys : int, optional
            ``0`` – global, ``1`` – local. Defaults to ``0``.
        """
        case = self._get_case_by_name(case_name)
        record_index = case.Records.New(self._rbt.IRobotLoadRecordType(22))
        record = case.Records.Get(record_index)
        record.Objects.FromText(str(objects))
        record.SetValue(0, loads[0])  # Px1
        record.SetValue(1, loads[1])  # Py1
        record.SetValue(2, loads[2])  # Pz1
        record.SetValue(3, loads[3])  # Px2
        record.SetValue(4, loads[4])  # Py2
        record.SetValue(5, loads[5])  # Pz2
        record.SetValue(6, loads[6])  # Px3
        record.SetValue(7, loads[7])  # Py3
        record.SetValue(8, loads[8])  # Pz3
        record.SetPoint(1, p1[0], p1[1], p1[2])
        record.SetPoint(2, p2[0], p2[1], p2[2])
        record.SetPoint(3, p3[0], p3[1], p3[2])
        record.SetValue(11, coord_sys)  # coord system
        record.SetValue(12, projected)  # projected

    def _get_case_by_name(self, case_name: str) -> Any:
        """Private function to get simple loadcase by name.

        Results are cached after the first lookup. The cache is keyed by name
        so repeated calls with the same case_name cost a single dict lookup
        instead of a full COM collection scan.

        Parameters
        ----------
            case_name: str
                Loadcase name

        Returns
        ----------
            IRobotCase
        """
        if case_name in self._case_cache:
            return self._case_cache[case_name]
        cases = self._cases.GetAll()
        for i in range(1, cases.Count + 1):
            lcase = self._rbt.IRobotCase(cases.Get(i))
            if lcase.Type == self._rbt.IRobotCaseType.I_CT_SIMPLE:
                if lcase.Name == case_name:
                    result = self._rbt.IRobotSimpleCase(lcase)
                    self._case_cache[case_name] = result
                    return result
        return None
