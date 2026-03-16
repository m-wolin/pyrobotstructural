from .bootstrap import get_robotom
from .model.facade import ModelFacade
from .loads.facade import LoadsFacade
from .query.facade import QueryFacade
from .view.facade import ViewFacade


class RobotApp:
    def __init__(self) -> None:
        rbt = get_robotom()
        self._raw = rbt.RobotApplication()

        self._model = ModelFacade(self._raw)
        self._loads = LoadsFacade(self._raw)
        self._query = QueryFacade(self._raw)
        self._view = ViewFacade(self._raw)

    @property
    def model(self) -> ModelFacade:
        return self._model

    @property
    def loads(self) -> LoadsFacade:
        return self._loads

    @property
    def query(self) -> QueryFacade:
        return self._query

    @property
    def view(self) -> ViewFacade:
        return self._view

    def calculate(self) -> None:
        """Triggers calculation of the model."""
        self._raw.Project.CalcEngine.Calculate()
