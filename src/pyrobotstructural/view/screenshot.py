import os
from typing import Any
from .save_screenshot import save_emf_as_png
from .._base import _BaseEditor
from .view import ViewManager


class ScreenshotManager(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._project = self._raw.Project

    def save_screenshot(self, name: str, dir_path: str, view: Any = None) -> None:
        """
        Takes a screenshot, stores it in clipboard and saves as .png under given path and name.

        Parameters
        ----------
        name: str
            Name of the image.
        dir_path: str
            Path of the directory, where screenshot is to be saved.
        view: IRobotView
            View of which screenshot to be taken.
        """
        if view is not None:
            current_view = view
        else:
            current_view = self._rbt.IRobotView3(self._project.ViewMngr.GetView(1))
        screen_params = self._rbt.IRobotViewScreenCaptureParams(
            self._raw.CmpntFactory.Create(
                self._rbt.IRobotComponentType.I_CT_VIEW_SCREEN_CAPTURE_PARAMS
            )
        )
        # screen_params.name = 'Test'
        screen_params.UpdateType = (
            self._rbt.IRobotViewScreenCaptureUpdateType.I_SCUT_COPY_TO_CLIPBOARD
        )

        current_view.MakeScreenCapture(screen_params)
        output_path = os.path.join(dir_path, name + ".png")
        save_emf_as_png(output_path)
