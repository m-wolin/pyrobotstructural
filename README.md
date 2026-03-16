# pyrobotstructural

A Python wrapper for [Autodesk Robot Structural Analysis Professional](https://www.autodesk.com/products/robot-structural-analysis/overview), providing a clean API for scripting structural models via the Robot COM interface.

## Requirements

- Windows
- Autodesk Robot Structural Analysis Professional (2023 or later)
- Python 3.14+

## Installation

```bash
uv sync
```

## Getting Started

Call `initialize()` once with the path to `Interop.RobotOM.dll` before using anything else. The path typically only needs a version number update:

```python
import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()
```

## API Overview

`RobotApp` exposes four facades:

| Property | Purpose |
|----------|---------|
| `app.model` | Create/edit geometry, sections, supports, releases |
| `app.loads` | Manage load cases, combinations, and applied loads |
| `app.query` | Read nodes, bars, cases, and analysis results |
| `app.view` | Control views and capture screenshots |

### Building a model

```python
app.model.management.clear()

# Add nodes: [id, x, y, z]
app.model.geometry.add_node([
    [1, 0.0, 0.0, 0.0],
    [2, 3.0, 0.0, 0.0],
])

# Add bars: [id, start_node, end_node]
app.model.geometry.add_member(
    [[1, 1, 2]],
    material_name="S235",
    section_name="IPE 100",
)

# Add a shell panel
app.model.geometry.add_shell_by_contour(
    points=[[1,0,0,0],[2,3,0,0],[3,3,3,0],[4,0,3,0]],
    thickness=0.1,
    thickness_name="10cm",
    material_name="C20/25",
)

# Apply supports
app.model.supports.apply_node_support(node_number=[1, 2], support_name="Pinned")
```

### Loads

```python
app.loads.cases.create_simple(1, "Self-weight", nature="permanent", solver="linear")
app.loads.load.add_self_weight(case_number=1)

app.loads.cases.create_simple(2, "Live load", nature="exploitation", solver="linear")
app.loads.load.add_uniform_load(case_number=2, value=-500, bar_selection="all")

app.loads.combinations.create(3, "ULS 1", factors={1: 1.35, 2: 1.5})
```

### Querying results

```python
nodes = app.query.nodes.get_all()
bars  = app.query.bars.get_all()
```

## Examples

The `examples/` directory contains step-by-step scripts:

| File | Description |
|------|-------------|
| `01_initialize.py` | Connect to Robot and verify with a single node |
| `02_build_geometry.py` | Nodes, bars, shells, cladding, supports |
| `03_loads.py` | Load cases, loads, and combinations |
| `04_view_control.py` | Manipulate the viewport |
| `05_query.py` | Read model data |
| `06_full_beam_example.py` | End-to-end: geometry → loads → calculation → screenshot |
