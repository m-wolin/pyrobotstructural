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

    def begin_edit(self):
        """Context manager that batches all structure modifications into a
        single multi-operation flush.  Delegates to
        ``app.model.geometry.begin_edit()``.

        Usage
        -----
        with app.model.begin_edit():
            app.model.geometry.add_node(nodes_array)
            app.model.geometry.add_member(members_array, section_name="IPE 100")
            app.model.supports.apply_node_support([1, 2], "Pinned")
        """
        return self.geometry.begin_edit()
