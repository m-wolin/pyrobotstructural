from typing import Any
import os
from .._base import _BaseEditor


class ModelQuery(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def get_model_path(self) -> str | Any:
        """Get Autodesk Robot model path.

        Returns
        ----------
        path: str
            Path of current (active) model.
        """
        filename = self._raw.Project.FileName
        if not filename:
            return os.getcwd()
        return os.path.dirname(filename)
