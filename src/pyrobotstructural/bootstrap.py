import clr
import importlib
from pathlib import Path


class _InteropState:
    loaded = False
    dll_path = None
    RobotOM = None


_state = _InteropState()


def initialize(dll_path: str) -> None:
    """
    Initialize pythonnet and load RobotOM.dll.
    Must be called once before using the library.
    """
    if _state.loaded:
        return

    path = Path(dll_path)

    if not path.exists():
        raise FileNotFoundError(f"RobotOM dll not found at {dll_path}")

    clr.AddReference(str(path))

    RobotOM = importlib.import_module("RobotOM")

    _state.RobotOM = RobotOM
    _state.dll_path = dll_path
    _state.loaded = True


def get_robotom() -> None:
    if not _state.loaded:
        raise RuntimeError(
            "pyrobotstructural not initialized. Call pyrobotstructural.initialize(dll_path) first."
        )
    return _state.RobotOM
