from typing import Any, Union
import numpy as np
from .._base import _BaseEditor
from ..enums import LabelType


class SupportEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels
        self._nodes = self._structure.Nodes

    def define_nodal_support(
        self, name: str, ux: int, uy: int, uz: int, rx: int, ry: int, rz: int
    ) -> None:
        """
        Creates a new support and adds it to the model.

        Parameters
        ----------
        name: str
            Name of the support
        ux: int
            Translation restraint direction x, 0 - free, 1 - full restraint
        uy: int
            Translation restraint direction y, 0 - free, 1 - full restraint
        uz: int
            Translation restraint direction z, 0 - free, 1 - full restraint
        rx: int
            Rotation restraint around x axis, 0 - free, 1 - full restraint
        ry: int
            Rotation restraint around y axis, 0 - free, 1 - full restraint
        rz: int
            Rotation restraint around y axis, 0 - free, 1 - full restraint
        """
        # TODO: add more flexibility ? for elastic and non-linear supports, one direction options
        # TODO: add other features based on Robot options? see what is possible
        support_label = self._labels.Create(
            self._rbt.IRobotLabelType.I_LT_SUPPORT, name
        )
        support_data = self._rbt.IRobotNodeSupportData(support_label.Data)
        support_data.UX = ux
        support_data.UY = uy
        support_data.UZ = uz
        support_data.RX = rx
        support_data.RY = ry
        support_data.RZ = rz
        self._labels.Store(support_label)

    def apply_support_to_edge(
        self, edge_name: str, support_name: str, edge_object: Any = None
    ) -> None:
        """
        You can applied support to edge, support can be nodal support.

        Parameters
        ----------
        edge_name: str
            Edge string name, it must be whole name for example... TODO: finish this text
        support_name: str
            Support name, assumes support exists
        edge_obect: IRobotObjEdge, optional
            Edge object can be optionally provided, make sure you proide IRobotObjEdge,
            edge_name  will be ignored.
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
        """Applies a support condition to one or more nodes.

        Parameters
        ----------
        node_number : int | list | np.ndarray
            A single node number, or a 1-D list/array of node numbers.
        support_name : str
            Support name — assumed to already exist in the model.

        Examples
        --------
        # Single node
        model.apply_node_support(1, "Pinned")

        # Multiple nodes — list or numpy array
        model.apply_node_support([1, 2, 3], "Pinned")
        model.apply_node_support(np.array([1, 2, 3]), "Pinned")
        """
        # --- normalise input to a flat list of ints ---
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

        # --- single pass over all nodes ---
        node_server = self._nodes.GetAll()
        for i in range(1, node_server.Count + 1):
            node = self._rbt.IRobotNode(node_server.Get(i))
            if node.Number in targets:
                node.SetLabel(LabelType.SUPPORT, support_name)
                targets.discard(node.Number)
                if not targets:  # stop early once all targets are matched
                    break

        if targets:
            raise ValueError(f"Node(s) not found in model: {sorted(targets)}")
