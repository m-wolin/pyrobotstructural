from typing import Any
from .screenshot import ScreenshotManager
from .view import ViewManager


class ViewFacade:
    """Facade for controlling the Robot viewport and capturing screenshots.

    Accessed via ``app.view``.  Aggregates the view control and screenshot
    managers.
    """

    def __init__(self, raw_app: Any) -> None:
        self._raw = raw_app
        self.screenshots = ScreenshotManager(self._raw)
        self.view = ViewManager(self._raw)
