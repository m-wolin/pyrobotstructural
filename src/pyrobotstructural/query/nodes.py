from typing import Any
from .._base import _BaseEditor


class NodesQuery(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._nodes = self._structure.Nodes

    def get_all(self, exclude_calc_nodes: bool = False) -> Any:
        """
        Gets all nodes in the Roboit Model

        Parameters
        ----------
        exclude_calc_nodes: bool, optional, default = False
            Trigger to include or include calculation nodes

        Returns
        ----------
            IRobotCollection of nodes (exclude_calc_nodes=False), or
            list[IRobotNode] (exclude_calc_nodes=True)
        """
        if exclude_calc_nodes:
            all_nodes = self._nodes.GetAll()
            nodes = []
            for node_index in range(1, all_nodes.Count + 1):
                node = self._rbt.IRobotNode(all_nodes.Get(node_index))
                if not node.IsCalc:
                    nodes.append(node)
            return nodes
        else:
            return self._nodes.GetAll()

    def get_all_in_list(self, exclude_calc_nodes: bool = False) -> list:
        """
        "Gets all nodes coordinates from Robot.

        Parameters
        ----------
        exclude_calc_nodes: bool, optional, default = False
            Trigger to include or include calculation nodes

        Returns
        ----------
            list[node_number, X, Y, Z]
        """
        node_coords = []
        if exclude_calc_nodes:
            # get_all returns a plain list when exclude_calc_nodes=True
            for node in self.get_all(exclude_calc_nodes=True):
                node_coords.append([node.Number, node.X, node.Y, node.Z])
        else:
            all_nodes = self._nodes.GetAll()
            for node_index in range(1, all_nodes.Count + 1):
                node = self._rbt.IRobotNode(all_nodes.Get(node_index))
                node_coords.append([node.Number, node.X, node.Y, node.Z])
        return node_coords

    def get_node(self, index: int, by_number: bool = False) -> Any:
        """
        Returns the node of given index.

        Parameters
        ----------
        index: int
            Index of a node
        by_number: bool, optional, default = False
            If node number instead of node index is to be used

        Returns
        ----------
            IRobotNode: object
        """
        node_collection = self.get_all()
        if by_number:
            for node_index in range(1, self._nodes.GetAll().Count + 1):
                node = self._rbt.IRobotNode(node_collection.Get(node_index))
                if node.Number == index:
                    return node
        else:
            node = self._rbt.IRobotNode(node_collection.Get(index))
            return node

    def get_compatible_nodes(self) -> Any:
        """
        Gets all nodes in the Robot Model.

        Returns
        ----------
          IRobotCollection: collection of nodes
        """
        return self._nodes.CompatibleNodes

    def get_node_coords(self, node: Any) -> list:
        """
        Returns coordinates of a node.

        Parameters
        ----------
        node: IRobotNode

        Returns
        ----------
          IRobotCollection: collection of nodes
        """
        return [node.X, node.Y, node.Z]
