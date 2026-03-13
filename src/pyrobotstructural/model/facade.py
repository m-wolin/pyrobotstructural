from typing import Any

from .geometry import GeometryEditor
from .sections import SectionEditor
from .supports import SupportEditor
from .management import ModelManager


class ModelFacade:
    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self.geometry = GeometryEditor(self._raw)
        self.sections = SectionEditor(self._raw)
        self.supports = SupportEditor(self._raw)
        self.management = ModelManager(self._raw)
