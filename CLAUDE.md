# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pyrobotstructural` is a Python wrapper for Autodesk Robot Structural Analysis Professional, using `pythonnet` (clr) to interop with the `RobotOM` COM API via a .NET DLL. **Windows-only.** Requires Robot Structural Analysis Professional to be installed.

## Commands

This project uses `uv` as the package manager.

```bash
# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/path/to/test_file.py::test_name

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy src/
```

## Architecture

### Initialization Flow

Before using the library, the user must call `initialize(dll_path)` once, which loads `RobotOM.dll` via `clr.AddReference` and stores the module in a singleton `_InteropState` (`bootstrap.py`). All classes retrieve the COM module via `get_robotom()`.

### Main Entry Point

`RobotApp` (`application.py`) wraps `rbt.RobotApplication()` and exposes four facade properties:

- `app.model` → `ModelFacade` — create/edit geometry, sections, supports, releases
- `app.loads` → `LoadsFacade` — load cases, load combinations, load application
- `app.query` → `QueryFacade` — read-only access to nodes, bars, cases, results
- `app.view` → `ViewFacade` — screenshots and view control

### Base Class

All editors/managers inherit from `_BaseEditor` (`_base.py`), which stores `self._raw` (the raw `RobotApplication` COM object) and `self._rbt` (the `RobotOM` module from `get_robotom()`).

### Enums Pattern

COM enums are wrapped as Python classes in `enums.py` using lazy descriptor objects (`_RobotEnumDescriptor`). Each enum class sets `_robot_enum_name` to the Robot COM interface name, and attributes are declared with `com_member("I_CONSTANT_NAME")`. The descriptor fetches the real COM value only when accessed, ensuring `initialize()` has been called first.

Example pattern for adding a new enum:
```python
class MyEnum:
    _robot_enum_name = "IRobotSomeEnumName"
    SOME_VALUE = com_member("I_SE_SOME_VALUE")
```

### Sub-package Structure

Each sub-package (`model/`, `loads/`, `query/`, `view/`) follows the same pattern:
- `facade.py` — aggregates sub-editors/managers as properties, takes `raw_app` in `__init__`
- Individual modules (e.g., `geometry.py`, `nodes.py`) — implement specific operations, inherit `_BaseEditor`

## Usage Example

```python
import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()
app.model.geometry.add_node(1, 0, 0, 0)
app.model.geometry.add_member([[1, 1, 2]], material_name="S235", section_name="IPE 100")
```

See `examples/` for more complete workflows.
