from typing import Any
from .save_screenshot import save_emf_as_png
from .._base import _BaseEditor


class ScreenshotManager(_BaseEditor):
    def __init__(self, raw_app: Any) -> None:
        super().__init__(raw_app)
        self._structure = self._raw.Project.Structure

    def save_screenshot(self, name: str, dir_path: str, view: Any) -> None:
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
        screen_params = self._rbt.IRobotViewScreenCaptureParams(
            self._raw.CmpntFactory.Create(
                self._rbt.IRobotComponentType.I_CT_VIEW_SCREEN_CAPTURE_PARAMS
            )
        )
        # screen_params.name = 'Test'
        screen_params.UpdateType = (
            self._rbt.IRobotViewScreenCaptureUpdateType.I_SCUT_COPY_TO_CLIPBOARD
        )

        view.MakeScreenCapture(screen_params)
        output_path = dir_path + "\\" + name + ".png"
        save_emf_as_png(output_path)
