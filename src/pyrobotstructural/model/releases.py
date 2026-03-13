from typing import Any
from .._base import _BaseEditor
from ..enums import LabelType


class ReleaseEditor(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure
        self._labels = self._structure.Labels

    def define_member_release(
        self,
        name: str,
        start_ux: int = 0,
        start_uy: int = 0,
        start_uz: int = 0,
        start_rx: int = 0,
        start_ry: int = 0,
        start_rz: int = 0,
        end_ux: int = 0,
        end_uy: int = 0,
        end_uz: int = 0,
        end_rx: int = 0,
        end_ry: int = 0,
        end_rz: int = 0,
    ) -> None:
        """Creates a member stndard linear release of given properties.
        TODO: Add more options, there can be damping, nonlinearity, elastic spring

        Parameters
        ----------
        name: str
            Name of the release.
        start_ux: int
            Start node release x axis, 0 - free, 1 - fixed.
        start_uy: int
            Start node release y axis, 0 - free, 1 - fixed.
        start_uz: int
            Start node release z axis, 0 - free, 1 - fixed.
        start_rx: int
            Start node release around x axis, 0 - free, 1 - fixed.
        start_ry: int
            Start node release around x axis, 0 - free, 1 - fixed.
        start_rz: int
            Start node release around x axis, 0 - free, 1 - fixed.
        end_ux: int
            End node release x axis, 0 - free, 1 - fixed.
        end_uy: int
            End node release y axis, 0 - free, 1 - fixed.
        end_uz: int
            End node release z axis, 0 - free, 1 - fixed.
        end_rx: int
            End node release around x axis, 0 - free, 1 - fixed.
        end_ry: int
            End node release around x axis, 0 - free, 1 - fixed.
        end_rz: int
            End node release around x axis, 0 - free, 1 - fixed.
        """
        label = self.labels.Create(LabelType.BAR_RELEASE, name)
        release_data = self._rbt.IRobotBarReleaseData(label.Data)
        release_data.StartNode.UX = self._rbt.IRobotBarEndReleaseValue(start_ux)
        release_data.StartNode.UY = self._rbt.IRobotBarEndReleaseValue(start_uy)
        release_data.StartNode.UZ = self._rbt.IRobotBarEndReleaseValue(start_uz)
        release_data.StartNode.RX = self._rbt.IRobotBarEndReleaseValue(start_rx)
        release_data.StartNode.RY = self._rbt.IRobotBarEndReleaseValue(start_ry)
        release_data.StartNode.RZ = self._rbt.IRobotBarEndReleaseValue(start_rz)
        release_data.EndNode.UX = self._rbt.IRobotBarEndReleaseValue(end_ux)
        release_data.EndNode.UY = self._rbt.IRobotBarEndReleaseValue(end_uy)
        release_data.EndNode.UZ = self._rbt.IRobotBarEndReleaseValue(end_uz)
        release_data.EndNode.RX = self._rbt.IRobotBarEndReleaseValue(end_rx)
        release_data.EndNode.RY = self._rbt.IRobotBarEndReleaseValue(end_ry)
        release_data.EndNode.RZ = self._rbt.IRobotBarEndReleaseValue(end_rz)
        self.labels.Store(label)

    def add_release_to_member(
        self,
        bar_number: int,
        release_name: str,
    ) -> None:
        """
        Adds relase to existing member.

        Parameters
        ----------
        bar_number : int
            Bar number.
        release_name: str
            Release name
        """
        bar = self._raw.IRobotBar(self._structure.Bars.Get(bar_number))
        bar.SetLabel(LabelType.BAR_RELEASE, release_name)

    def define_linear_realease(
        self,
        name: str,
        ux: int = 0,
        uy: int = 0,
        uz: int = 0,
        rx: int = 0,
        kx: float = None,
        ky: float = None,
        kz: float = None,
        hx: float = None,
    ) -> None:
        """
        Creates new linear release.

         Parameters
        ----------
        name: str,
            Name of the release
        ux: int, default=0
            Release for x direction, if 1 then full release, if 2 then release in direction opposite to
            the local system on the panel edge. 3 then release in direction with local system on the panel edge.
        uy: int, default=0
            Release for y direction, if 1 then full release, if 2 then release in direction opposite to
            the local system on the panel edge.
        uz: int, default=0
            Release for y direction, if 1 then full release, if 2 then release in direction opposite to
            the local system on the panel edge. 3 then release in direction with local system on the panel edge.
        rx: int, default=0
            Release for rotation around x axis, if 1 then full release, if 2 then release in direction opposite to
            the local system on the panel edge. 3 then release in direction with local system on the panel edge.
        kx: float, optional
            Elastic release value in direction x, if applied, then ux value is ignored.
        kx: float, optional
            Elastic release value in direction y, if applied, then ux value is ignored.
        kx: float, optional
            Elastic release value in direction z, if applied, then ux value is ignored.
        hx: float, optional
            Elastic release for rotation around x axis, if applied, then ux value is ignored.
        """
        label = self.labels.Create(LabelType.LINEAR_RELEASE, name)
        release_data = self._rbt.IRobotLinearReleaseData(label.Data)

        if kx is not None:
            release_data.KX = kx
        else:
            release_data.UX = ux
        if ky is not None:
            release_data.KY = ky
        else:
            release_data.UY = uy
        if kz is not None:
            release_data.KZ = kz
        else:
            release_data.UZ = uz
        if hx is not None:
            release_data.HX = hx
        else:
            release_data.RX = rx

    def add_linear_release_to_edge(self) -> None:
        pass
