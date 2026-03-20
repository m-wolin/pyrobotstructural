# pyrobotstructural

An **unofficial** Python wrapper for [Autodesk Robot Structural Analysis Professional](https://www.autodesk.com/products/robot-structural-analysis/overview),
providing a clean Pythonic API for scripting structural models via the Robot COM interface.

```{note}
Windows-only. Requires Autodesk Robot Structural Analysis Professional to be installed.
```

## Installation

```bash
pip install pyrobotstructural
```

Or install the latest version directly from GitHub:

```bash
pip install git+https://github.com/m-wolin/pyrobotstructural
```

## Quick start

```python
import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()
app.model.geometry.add_node(1, 0, 0, 0)
```

## Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

getting_started
examples
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/index
```
