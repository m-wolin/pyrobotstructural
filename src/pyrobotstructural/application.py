from .bootstrap import get_robotom
from .model.facade import ModelFacade
from .loads.facade import LoadsFacade
from .query.facade import QueryFacade
from .view.facade import ViewFacade


class RobotApp:
    """Main entry point for pyrobotstructural.

    Wraps ``RobotApplication`` (the root COM object) and exposes four
    sub-facades as properties.  Call :func:`pyrobotstructural.initialize`
    once with the path to ``Interop.RobotOM.dll`` before instantiating
    this class.

    Examples
    --------
    >>> import pyrobotstructural
    >>> dll = r"C:\\Program Files\\Autodesk\\Robot Structural Analysis Professional 2026\\Exe\\Interop.RobotOM.dll"
    >>> pyrobotstructural.initialize(dll)
    >>> app = pyrobotstructural.RobotApp()
    >>> app.model.geometry.add_node(1, 0, 0, 0)
    >>> app.calculate()
    """

    def __init__(self) -> None:
        rbt = get_robotom()
        self._raw = rbt.RobotApplication()

        self._model = ModelFacade(self._raw)
        self._loads = LoadsFacade(self._raw)
        self._query = QueryFacade(self._raw)
        self._view = ViewFacade(self._raw)

    @property
    def model(self) -> ModelFacade:
        """Facade for creating and editing the structural model.

        Provides access to:

        - ``geometry`` — nodes, bars, shells, cladding
        - ``sections`` — cross-section definitions
        - ``supports`` — nodal support definitions and assignment
        - ``management`` — clear model, project management

        Use ``app.model.begin_edit()`` as a context manager when adding many
        objects at once to batch COM calls for significantly better performance.
        """
        return self._model

    @property
    def loads(self) -> LoadsFacade:
        """Facade for managing load cases, combinations, and applied loads.

        Provides access to:

        - ``cases`` — create and manage load cases
        - ``combinations`` — create ULS/SLS combinations
        - ``load`` — apply loads (self-weight, nodal, uniform, panel, etc.)
        """
        return self._loads

    @property
    def query(self) -> QueryFacade:
        """Read-only facade for querying the model and analysis results.

        Provides access to:

        - ``nodes`` — node coordinates and metadata
        - ``bars`` — bar topology and section data
        - ``loadcases`` — list and access load cases
        - ``combinations`` — list and access combinations
        - ``model`` — model file path and metadata
        - ``results`` — bar member forces, deflections, and stresses
        - ``shell_results`` — shell FE element forces and stresses
        """
        return self._query

    @property
    def view(self) -> ViewFacade:
        """Facade for controlling the Robot viewport and capturing screenshots.

        Provides access to:

        - ``view`` — display controls, results visualisation, zoom/pan/rotate
        - ``screenshots`` — capture and save view screenshots as PNG
        """
        return self._view

    def calculate(self, ignore_warnings: bool = False) -> None:
        """Run the structural analysis.

        Parameters
        ----------
        ignore_warnings : bool, optional
            If ``True``, analysis warnings are suppressed and the solver
            continues without stopping.  Defaults to ``False``.
        """
        calc_engine = self._raw.Project.CalcEngine
        if ignore_warnings:
            analysis_params = calc_engine.AnalysisParams
            analysis_params.IgnoreWarnings = True
        calc_engine.Calculate()
