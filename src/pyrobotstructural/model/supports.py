from typing import Any, Optional, Union
import numpy as np
from .._base import _BaseEditor
from ..enums import LabelType, NodeSupportFixingDir, NodeSupportOneDirType


# Maps lowercase DOF name -> NodeSupportFixingDir attribute name
_DOF_TO_FIXING_DIR: dict[str, str] = {
    "ux": "UX",
    "uy": "UY",
    "uz": "UZ",
    "rx": "RX",
    "ry": "RY",
    "rz": "RZ",
}

# Maps user-facing one-dir string -> NodeSupportOneDirType attribute name
_ONE_DIR_STR_TO_TYPE: dict[str, str] = {
    "+": "PLUS",
    "plus": "PLUS",
    "-": "MINUS",
    "minus": "MINUS",
}


class SupportEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._nodes = self._structure.Nodes

    def define_nodal_support(
        self,
        name: str,
        *,
        ux: int = 0,
        uy: int = 0,
        uz: int = 0,
        rx: int = 0,
        ry: int = 0,
        rz: int = 0,
        kx: float = 0.0,
        ky: float = 0.0,
        kz: float = 0.0,
        hx: float = 0.0,
        hy: float = 0.0,
        hz: float = 0.0,
        one_dir: Optional[dict[str, str]] = None,
        alpha: float = 0.0,
        beta: float = 0.0,
        gamma: float = 0.0,
    ) -> None:
        """Create a nodal support label and store it in the model.

        Supports three independent restraint mechanisms per DOF — rigid fixity,
        elastic spring, and one-directional (unilateral) blocking.  They can be
        combined freely: e.g. a direction can be both elastically restrained
        *and* one-directional (tension-only spring).

        Parameters
        ----------
        name : str
            Label name for this support.  Must be unique within the model.
        ux : int, optional
            Rigid restraint in X translation.  ``0`` = free, ``1`` = fully fixed.
        uy : int, optional
            Rigid restraint in Y translation.
        uz : int, optional
            Rigid restraint in Z translation.
        rx : int, optional
            Rigid restraint about X axis.
        ry : int, optional
            Rigid restraint about Y axis.
        rz : int, optional
            Rigid restraint about Z axis.
        kx : float, optional
            Translational elastic spring stiffness in X [kN/m].  ``0.0`` = not used.
        ky : float, optional
            Translational elastic spring stiffness in Y [kN/m].
        kz : float, optional
            Translational elastic spring stiffness in Z [kN/m].
        hx : float, optional
            Rotational elastic spring stiffness about X [kNm/rad].  ``0.0`` = not used.
        hy : float, optional
            Rotational elastic spring stiffness about Y [kNm/rad].
        hz : float, optional
            Rotational elastic spring stiffness about Z [kNm/rad].
        one_dir : dict[str, str], optional
            One-directional (unilateral) blocking.  Keys are DOF names
            (``"ux"``, ``"uy"``, ``"uz"``, ``"rx"``, ``"ry"``, ``"rz"``).
            Values are ``"+"`` / ``"plus"`` (resists positive displacement only)
            or ``"-"`` / ``"minus"`` (resists negative displacement only).

            Example::

                one_dir={"uz": "-"}  # compression-only foundation (resists downward)

        alpha : float, optional
            Rotation of support local axes about global Z [rad].  ``0.0`` = aligned
            with global axes.
        beta : float, optional
            Rotation of support local axes about global Y [rad].
        gamma : float, optional
            Rotation of support local axes about global X [rad].

        Raises
        ------
        ValueError
            If ``one_dir`` contains an unknown DOF key or direction string.

        Examples
        --------
        Pinned support (UX, UY, UZ fixed, rotations free):

        >>> app.model.supports.define_nodal_support("Pinned", ux=1, uy=1, uz=1)

        Roller in Z with elastic spring in X (1000 kN/m):

        >>> app.model.supports.define_nodal_support("SpringX", uz=1, kx=1000.0)

        Compression-only (one-directional) support in Z:

        >>> app.model.supports.define_nodal_support("CompOnly", one_dir={"uz": "-"})

        Combined elastic + one-directional (tension-only spring in Z):

        >>> app.model.supports.define_nodal_support(
        ...     "TensionSpringZ", kz=5000.0, one_dir={"uz": "+"}
        ... )
        """
        support_label = self._labels.Create(
            self._rbt.IRobotLabelType.I_LT_SUPPORT, name
        )
        sd = self._rbt.IRobotNodeSupportData(support_label.Data)

        # --- Rigid fixity ---
        sd.UX = ux
        sd.UY = uy
        sd.UZ = uz
        sd.RX = rx
        sd.RY = ry
        sd.RZ = rz

        # --- Elastic springs ---
        if kx:
            sd.KX = kx
        if ky:
            sd.KY = ky
        if kz:
            sd.KZ = kz
        if hx:
            sd.HX = hx
        if hy:
            sd.HY = hy
        if hz:
            sd.HZ = hz

        # --- Local axis orientation ---
        if alpha:
            sd.Alpha = alpha
        if beta:
            sd.Beta = beta
        if gamma:
            sd.Gamma = gamma

        # --- One-directional (unilateral) blocking ---
        if one_dir:
            self._apply_one_dir(sd, one_dir)

        self._labels.Store(support_label)

    def _apply_one_dir(
        self,
        support_data: Any,
        one_dir: dict[str, str],
    ) -> None:
        """Apply one-directional blocking entries to *support_data*.

        Parameters
        ----------
        support_data : IRobotNodeSupportData
            The COM support data object to configure.
        one_dir : dict[str, str]
            Mapping of DOF name to direction string (``"+"``/``"-"``).

        Raises
        ------
        ValueError
            If a DOF key or direction string is not recognised.
        """
        for dof, direction in one_dir.items():
            dof_key = dof.lower()
            if dof_key not in _DOF_TO_FIXING_DIR:
                raise ValueError(
                    f"Unknown DOF '{dof}' in one_dir. "
                    f"Must be one of: {list(_DOF_TO_FIXING_DIR)}"
                )
            dir_key = direction.lower() if isinstance(direction, str) else str(direction)
            if dir_key not in _ONE_DIR_STR_TO_TYPE:
                raise ValueError(
                    f"Unknown one-dir direction '{direction}'. "
                    f"Use '+', 'plus', '-', or 'minus'."
                )
            fixing_dir = getattr(NodeSupportFixingDir, _DOF_TO_FIXING_DIR[dof_key])
            one_dir_type = getattr(NodeSupportOneDirType, _ONE_DIR_STR_TO_TYPE[dir_key])
            support_data.SetOneDir(fixing_dir, one_dir_type)

    def apply_support_to_edge(
        self, edge_name: str, support_name: str, edge_object: Any = None
    ) -> None:
        """Apply a support label to an edge.

        Parameters
        ----------
        edge_name : str
            Edge string name, it must be whole name for example... TODO: finish this text
        support_name : str
            Support name, assumes support exists
        edge_object : IRobotObjEdge, optional
            Edge object can be optionally provided, make sure you provide IRobotObjEdge,
            edge_name will be ignored.
        """
        if edge_object is None:
            edge_selection = (
                self._structure.IRobotSelectionFactory.CreateEdgeSelection()
            )
            edge_selection.FromText(edge_name)
            if edge_selection.Count > 0:
                for n in range(1, edge_selection.Count + 1):
                    edge = edge_selection.Get(n)
                    edge.SetLabel(LabelType.SUPPORT, support_name)
        else:
            edge_object.SetLabel(LabelType.SUPPORT, support_name)

    def apply_node_support(
        self,
        node_number: Union[int, list, np.ndarray],
        support_name: str,
    ) -> None:
        """Apply a support condition to one or more nodes.

        Parameters
        ----------
        node_number : int | list | np.ndarray
            A single node number, or a 1-D list/array of node numbers.
        support_name : str
            Support name — assumed to already exist in the model.

        Examples
        --------
        Single node:

        >>> app.model.supports.apply_node_support(1, "Pinned")

        Multiple nodes — list or numpy array:

        >>> app.model.supports.apply_node_support([1, 2, 3], "Pinned")
        >>> app.model.supports.apply_node_support(np.array([1, 2, 3]), "Pinned")
        """
        if isinstance(node_number, (int, np.integer)):
            targets = {int(node_number)}
        elif isinstance(node_number, (list, np.ndarray)):
            arr = np.asarray(node_number)
            if arr.ndim != 1:
                raise ValueError(
                    f"node_number array must be 1-D, got shape {arr.shape}."
                )
            targets = {int(n) for n in arr}
        else:
            raise TypeError(
                f"Expected int, list, or np.ndarray, got {type(node_number).__name__}."
            )

        node_server = self._nodes.GetAll()
        for i in range(1, node_server.Count + 1):
            node = self._rbt.IRobotNode(node_server.Get(i))
            if node.Number in targets:
                node.SetLabel(LabelType.SUPPORT, support_name)
                targets.discard(node.Number)
                if not targets:
                    break

        if targets:
            raise ValueError(f"Node(s) not found in model: {sorted(targets)}")
