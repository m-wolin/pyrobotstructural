# pyrobotstructural

An **UNOFFICIAL** Python wrapper for [Autodesk Robot Structural Analysis Professional](https://www.autodesk.com/products/robot-structural-analysis/overview), providing a clean API for scripting structural models via the Robot COM interface.

Not all functionality is implemented, however the wrapper should cover the most used functions. It allows to:
- create geometry
- add loads, cases and combinations
- calculate the model
- read objects and results

Feel free to suggest improvements or report an issue.

## Requirements

- Windows
- Autodesk Robot Structural Analysis Professional (2018 or later, although any version should work)
- Python 3.14+

## Installation

```bash
pip install pyrobotstructural
```
Or install directly latest version from GitHub:
```bash
pip install git+https://github.com/m-wolin/pyrobotstructural
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

`RobotApp` exposes four facades plus a calculate method:

| Property / Method | Purpose |
|-------------------|---------|
| `app.model` | Create/edit geometry, sections, supports, releases |
| `app.loads` | Manage load cases, combinations, and applied loads |
| `app.query` | Read nodes, bars, cases, and analysis results |
| `app.view` | Control views and capture screenshots |
| `app.calculate()` | Run structural analysis |

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

Use the `begin_edit()` context manager when adding many objects at once for a significant performance boost:

```python
with app.model.begin_edit():
    for i, (x, y, z) in enumerate(coords, start=1):
        app.model.geometry.add_node([[i, x, y, z]])
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

# Bar member results (forces, deflections, stresses)
results = app.query.results.get_forces(bar_id=1, case_number=2)

# Shell element results
shell_res = app.query.shell_results.get_forces(case_number=2)
```

## Code Structure

```
src/pyrobotstructural/
├── bootstrap.py          # initialize() and singleton interop state
├── application.py        # RobotApp main entry point
├── _base.py              # _BaseEditor base class
├── enums.py              # COM enum wrappers (lazy descriptor pattern)
│
├── model/
│   ├── facade.py         # ModelFacade
│   ├── geometry.py       # Nodes, bars, shells, cladding
│   ├── sections.py       # Cross-section creation
│   ├── supports.py       # Nodal support definitions and assignment
│   ├── releases.py       # Member end releases
│   └── management.py     # Clear model, project management
│
├── loads/
│   ├── facade.py         # LoadsFacade
│   ├── cases.py          # Load case creation and management
│   ├── combinations.py   # ULS/SLS combination creation
│   └── load.py           # Load application (self-weight, nodal, uniform, panel)
│
├── query/
│   ├── facade.py         # QueryFacade (read-only)
│   ├── nodes.py          # Node coordinate queries
│   ├── bars.py           # Bar topology and section queries
│   ├── loadcases.py      # Load case queries
│   ├── combinations.py   # Combination queries
│   ├── model.py          # Model metadata and file paths
│   ├── results.py        # Bar and shell results (forces, stresses, deflections)
│   └── _latex.py         # LaTeX report generation
│
└── view/
    ├── facade.py         # ViewFacade
    ├── view.py           # Display controls, results visualization
    └── screenshot.py     # Screenshot capture and saving
```

## Examples

The `examples/` directory contains step-by-step scripts:

| File | Description |
|------|-------------|
| `01_initialize.py` | Connect to Robot and verify with a single node |
| `02_build_geometry.py` | Nodes, bars, shells, cladding, and `begin_edit()` for bulk performance |
| `03_loads.py` | Load cases, load types, and combinations |
| `04_view_control.py` | Viewport manipulation, display toggles, results visualization |
| `05_query.py` | Read model data: nodes, bars, load cases, combinations |
| `05a_query_member_results.py` | Bar forces, deflections, stresses, and envelopes |
| `05b_query_shell_results.py` | Shell element forces and stresses (Nxx, Myy, von Mises, etc.) |
| `06_beam_example.py` | End-to-end: geometry → loads → calculation → screenshot |
| `07_supports.py` | Rigid, elastic spring, one-directional, and skewed support types |
| `08_lattice_tower.py` | Parametric lattice tower — bulk geometry with `begin_edit()` |
| `09_cladding_local_cs.py` | Cladding panels with custom local coordinate systems |
| `10_sections.py` | Custom sections: CHS tubes, solid/hollow rectangles |


## Extend beyond pyrobostructural functionality
Wrapper does not contain all possible Robot API functionality, however, you can write your own code using the 'raw' objects.

To access 'raw' application object use:
```python
app._raw # Returns RobotApplication object
```

To access RobotOM dll (equivalent of import RobotOM as rbt)
```python
app._rbt # Returns RobotOM
```
From this point you can access app._raw.Project and with app._rbt you can access Enums and interfaces.
