import math
from dataclasses import dataclass
from typing import Any

from .._base import _BaseEditor
from ..enums import ShellLayer


@dataclass
class MemberForces:
    """Internal forces at a single point on a bar member.

    All values are returned in Robot's internal SI units.

    Attributes
    ----------
    fx : float
        Axial force [N].
    fy : float
        Shear force in the local Y direction [N].
    fz : float
        Shear force in the local Z direction [N].
    mx : float
        Torsional moment about the local X axis [Nm].
    my : float
        Bending moment about the local Y axis [Nm].
    mz : float
        Bending moment about the local Z axis [Nm].
    """

    fx: float
    fy: float
    fz: float
    mx: float
    my: float
    mz: float


@dataclass
class MemberDeflection:
    """Displacements and rotations at a single point on a bar member.

    All values are returned in Robot's internal SI units.

    Attributes
    ----------
    ux : float
        Displacement in the global X direction [m].
    uy : float
        Displacement in the global Y direction [m].
    uz : float
        Displacement in the global Z direction [m].
    rx : float
        Rotation about the global X axis [rad].
    ry : float
        Rotation about the global Y axis [rad].
    rz : float
        Rotation about the global Z axis [rad].
    """

    ux: float
    uy: float
    uz: float
    rx: float
    ry: float
    rz: float


@dataclass
class MemberStress:
    """Cross-section stresses at a single point on a bar member.

    All values are returned in Robot's internal SI units.

    Attributes
    ----------
    smax : float
        Maximum normal stress (tension positive) [Pa].
    smin : float
        Minimum normal stress (compression negative) [Pa].
    shear_y : float
        Shear stress in the local Y direction [Pa].
    shear_z : float
        Shear stress in the local Z direction [Pa].
    torsion : float
        Torsional shear stress [Pa].
    """

    smax: float
    smin: float
    shear_y: float
    shear_z: float
    torsion: float


class BarResultsQuery(_BaseEditor):
    """Read-only access to bar member analysis results.

    Wraps ``IRobotBarResultServer`` (``Project.Structure.Results.Bars``) and
    exposes internal forces, displacements, and stresses for individual bars
    and load cases.

    Access path: ``app.query.results``

    Parameters
    ----------
    raw_app : Any
        The raw ``RobotApplication`` COM object passed down from
        ``RobotApp``.
    """

    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def _bar_result_server(self) -> Any:
        return self._rbt.IRobotBarResultServer(self._structure.Results.Bars)

    # ------------------------------------------------------------------
    # Forces
    # ------------------------------------------------------------------

    def get_forces(
        self, bar_number: int, case_number: int, position: float = 0.5
    ) -> MemberForces:
        """Return internal forces at a single position along the bar.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.
        position : float, optional
            Relative position along the bar, ``0.0`` (start) to ``1.0``
            (end). Defaults to ``0.5`` (midspan).

        Returns
        -------
        MemberForces
            Internal forces at the requested position.
        """
        server = self._bar_result_server()
        data = self._rbt.IRobotBarForceData(
            server.Forces.Value(bar_number, case_number, position)
        )
        return MemberForces(
            fx=data.FX,
            fy=data.FY,
            fz=data.FZ,
            mx=data.MX,
            my=data.MY,
            mz=data.MZ,
        )

    def get_forces_at_points(
        self, bar_number: int, case_number: int, n_points: int = 5
    ) -> list[MemberForces]:
        """Return internal forces at evenly-spaced points along the bar.

        Points are numbered 1 to ``n_points`` by Robot's
        ``ValueByNPoints`` method, which spaces them uniformly from the
        start node to the end node.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.
        n_points : int, optional
            Number of evenly-spaced evaluation points. Defaults to ``5``.

        Returns
        -------
        list[MemberForces]
            Forces at each point, ordered from start to end of the bar.
        """
        server = self._bar_result_server()
        results = []
        for i in range(1, n_points + 1):
            data = self._rbt.IRobotBarForceData(
                server.Forces.ValueByNPoints(bar_number, case_number, n_points, i)
            )
            results.append(
                MemberForces(
                    fx=data.FX,
                    fy=data.FY,
                    fz=data.FZ,
                    mx=data.MX,
                    my=data.MY,
                    mz=data.MZ,
                )
            )
        return results

    # ------------------------------------------------------------------
    # Deflections / Displacements
    # ------------------------------------------------------------------

    def get_deflections(
        self, bar_number: int, case_number: int, position: float = 0.5
    ) -> MemberDeflection:
        """Return deflection at a single position along the bar.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.
        position : float, optional
            Relative position along the bar, ``0.0`` (start) to ``1.0``
            (end). Defaults to ``0.5`` (midspan).

        Returns
        -------
        MemberDeflection
            Deflection at the requested position. Rotation fields are set to 0
            as ``RobotBarDeflectionData`` does not expose them.
        """
        server = self._bar_result_server()
        data = server.Deflections.Value(bar_number, case_number, position)
        # data = server.Deflections.Value(bar_number, position, case_number)
        # print(data.PosUZ)

        return MemberDeflection(
            ux=data.UX,
            uy=data.UY,
            uz=data.UZ,
            rx=0.0,
            ry=0.0,
            rz=0.0,
        )

    def get_max_deflection(self, bar_number: int, case_number: int) -> MemberDeflection:
        """Return max deflection in the bar.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.

        Returns
        -------
        MemberDeflection
            Maximum displacements (UX, UY, UZ). Rotation fields are set to 0
            as ``RobotBarDeflectionData`` does not expose them.
        """
        server = self._bar_result_server()
        data = server.Deflections.MaxValue(bar_number, case_number)
        return MemberDeflection(
            ux=data.UX, uy=data.UY, uz=data.UZ, rx=0.0, ry=0.0, rz=0.0
        )

    # ------------------------------------------------------------------
    # Stresses
    # ------------------------------------------------------------------

    def get_stresses(
        self, bar_number: int, case_number: int, pos: float = 0.5
    ) -> MemberStress:
        """Return cross-section stresses at a single position along the bar.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.
        pos : float, optional
            Relative position along the bar, ``0.0`` (start) to ``1.0``
            (end). Defaults to ``0.5`` (midspan).

        Returns
        -------
        MemberStress
            Cross-section stresses at the requested position.
        """
        server = self._bar_result_server()
        data = self._rbt.IRobotBarStressData(
            server.Stresses.Value(bar_number, case_number, pos)
        )
        return MemberStress(
            smax=data.Smax,
            smin=data.Smin,
            shear_y=data.ShearY,
            shear_z=data.ShearZ,
            torsion=data.Torsion,
        )

    def get_stresses_at_points(
        self, bar_number: int, case_number: int, n_points: int = 5
    ) -> list[MemberStress]:
        """Return cross-section stresses at evenly-spaced points along the bar.

        Parameters
        ----------
        bar_number : int
            Robot bar number.
        case_number : int
            Load case or combination number.
        n_points : int, optional
            Number of evenly-spaced evaluation points. Defaults to ``5``.

        Returns
        -------
        list[MemberStress]
            Stresses at each point, ordered from start to end of the bar.
        """
        server = self._bar_result_server()
        results = []
        for i in range(n_points):
            pos = i / (n_points - 1) if n_points > 1 else 0.5
            data = self._rbt.IRobotBarStressData(
                server.Stresses.Value(bar_number, case_number, pos)
            )
            results.append(
                MemberStress(
                    smax=data.Smax,
                    smin=data.Smin,
                    shear_y=data.ShearY,
                    shear_z=data.ShearZ,
                    torsion=data.Torsion,
                )
            )
        return results


# ---------------------------------------------------------------------------
# Shell (planar FE) result types
# ---------------------------------------------------------------------------


@dataclass
class ShellForces:
    """In-plane forces and moments per unit width for a shell finite element.

    Values correspond to the fields of ``IRobotFeResultDetailed`` and are
    expressed per unit width of the shell mid-plane.

    Attributes
    ----------
    nxx : float
        Membrane (normal) force in the local X direction [N/m].
    nyy : float
        Membrane (normal) force in the local Y direction [N/m].
    nxy : float
        Membrane shear force [N/m].
    mxx : float
        Bending moment about the local Y axis per unit width [Nm/m].
    myy : float
        Bending moment about the local X axis per unit width [Nm/m].
    mxy : float
        Torsional (twisting) moment per unit width [Nm/m].
    qxx : float
        Transverse shear force in the local X direction [N/m].
    qyy : float
        Transverse shear force in the local Y direction [N/m].
    """

    nxx: float
    nyy: float
    nxy: float
    mxx: float
    myy: float
    mxy: float
    qxx: float
    qyy: float


@dataclass
class ShellStresses:
    """In-plane and transverse stresses for a shell finite element.

    Values correspond to the fields of ``IRobotFeResultDetailed``.
    Von Mises stress is computed from the Cauchy in-plane components.

    Attributes
    ----------
    sxx : float
        Normal stress in the local X direction, σxx [Pa].
    syy : float
        Normal stress in the local Y direction, σyy [Pa].
    sxy : float
        In-plane shear stress, τxy [Pa].
    txx : float
        Transverse shear stress in the local X direction [Pa].
    tyy : float
        Transverse shear stress in the local Y direction [Pa].
    mises : float
        Von Mises equivalent stress [Pa], computed as
        ``sqrt(σxx² + σyy² − σxx·σyy + 3·τxy²)``.
    """

    sxx: float
    syy: float
    sxy: float
    txx: float
    tyy: float
    mises: float


class ShellResultsQuery(_BaseEditor):
    """Read-only access to planar shell finite element analysis results.

    Wraps ``IRobotFeResultServer``
    (``Project.Structure.Results.FiniteElems``) and exposes in-plane
    forces and stresses for individual FE elements, load cases, and
    through-thickness layers.

    Access path: ``app.query.shell_results``

    Parameters
    ----------
    raw_app : Any
        The raw ``RobotApplication`` COM object passed down from
        ``RobotApp``.

    Notes
    -----
    Results are retrieved via ``IRobotFeResultDetailed``, which requires
    an ``IRobotFeResultParams`` object specifying the element number, load
    case, and through-thickness layer. Use :class:`~pyrobotstructural.enums.ShellLayer`
    constants to select the layer:

    - ``ShellLayer.TOP`` — upper (top) surface
    - ``ShellLayer.MID`` — mid-plane (default)
    - ``ShellLayer.BOTTOM`` — lower (bottom) surface
    """

    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def _fe_result_server(self) -> Any:
        return self._rbt.IRobotFeResultServer(self._structure.Results.FiniteElems)

    def _make_params(
        self,
        element_number: int,
        case_number: int,
        layer: Any,
    ) -> Any:
        params = self._rbt.RobotFeResultParams()
        params.Case = case_number
        params.Element = element_number
        params.Layer = layer
        # params.Node = node_number
        return params

    # ------------------------------------------------------------------
    # Forces
    # ------------------------------------------------------------------

    def get_forces(
        self,
        element_number: int,
        case_number: int,
        layer: Any = None,
    ) -> ShellForces:
        """Return in-plane forces and moments for a single FE element.

        Parameters
        ----------
        element_number : int
            Finite element number in Robot.
        case_number : int
            Load case or combination number.
        layer : ShellLayer or None, optional
            Through-thickness layer at which results are evaluated.
            Accepts ``ShellLayer.TOP``, ``ShellLayer.MID``, or
            ``ShellLayer.BOTTOM``. Defaults to ``ShellLayer.MID``.

        Returns
        -------
        ShellForces
            In-plane forces and moments per unit width at the requested
            layer.
        """
        if layer is None:
            layer = ShellLayer.MID
        params = self._make_params(element_number, case_number, layer)
        data = self._rbt.IRobotFeResultDetailed(
            self._fe_result_server().Detailed(params)
        )
        return ShellForces(
            nxx=data.NXX,
            nyy=data.NYY,
            nxy=data.NXY,
            mxx=data.MXX,
            myy=data.MYY,
            mxy=data.MXY,
            qxx=data.QXX,
            qyy=data.QYY,
        )

    # ------------------------------------------------------------------
    # Stresses
    # ------------------------------------------------------------------

    def get_stresses(
        self,
        element_number: int,
        case_number: int,
        layer: Any = None,
    ) -> ShellStresses:
        """Return in-plane stresses (including von Mises) for a single FE element.

        Parameters
        ----------
        element_number : int
            Finite element number in Robot.
        case_number : int
            Load case or combination number.
        layer : ShellLayer or None, optional
            Through-thickness layer at which results are evaluated.
            Accepts ``ShellLayer.TOP``, ``ShellLayer.MID``, or
            ``ShellLayer.BOTTOM``. Defaults to ``ShellLayer.MID``.

        Returns
        -------
        ShellStresses
            In-plane and transverse stresses at the requested layer,
            including the computed von Mises stress.

        Notes
        -----
        Von Mises stress is derived from the Cauchy in-plane stress
        components using the plane-stress formula:

        .. math::

            \\sigma_{vm} = \\sqrt{\\sigma_{xx}^2 + \\sigma_{yy}^2
                          - \\sigma_{xx}\\,\\sigma_{yy} + 3\\,\\tau_{xy}^2}
        """
        if layer is None:
            layer = ShellLayer.MID
        params = self._make_params(element_number, case_number, layer)
        data = self._rbt.IRobotFeResultDetailed(
            self._fe_result_server().Detailed(params)
        )
        sxx, syy, sxy = data.SXX, data.SYY, data.SXY
        mises = math.sqrt(sxx**2 + syy**2 - sxx * syy + 3.0 * sxy**2)
        return ShellStresses(
            sxx=sxx,
            syy=syy,
            sxy=sxy,
            txx=data.TXX,
            tyy=data.TYY,
            mises=mises,
        )
