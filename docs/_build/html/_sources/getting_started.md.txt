# Getting Started

## Requirements

- **Windows** (Robot Structural Analysis Professional is Windows-only)
- **Autodesk Robot Structural Analysis Professional** 2018 or later
- **Python 3.14+**

## Installation

```bash
pip install pyrobotstructural
```

## Initialization

Before using anything else, call `initialize()` once with the path to
`Interop.RobotOM.dll`. The only part of the path that typically needs
updating between Robot versions is the year number:

```python
import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)
```

This loads the Robot COM module via `pythonnet` and stores it in a singleton
so the call is a no-op if made more than once.

## Creating an application handle

```python
app = pyrobotstructural.RobotApp()
```

`RobotApp` connects to the running Robot instance and exposes four facades:

| Property | Purpose |
|----------|---------|
| `app.model` | Create/edit geometry, sections, supports |
| `app.loads` | Load cases, combinations, applied loads |
| `app.query` | Read nodes, bars, cases, results |
| `app.view` | Viewport control and screenshots |

## Building a model

### Nodes and bars

```python
app.model.management.clear()

# Single node
app.model.geometry.add_node(1, 0.0, 0.0, 0.0)

# Multiple nodes — 2-D list [number, x, y, z]
app.model.geometry.add_node([
    [2, 3.0, 0.0, 0.0],
    [3, 6.0, 0.0, 0.0],
])

# Bars — [number, start_node, end_node]
app.model.geometry.add_member(
    [[1, 1, 2], [2, 2, 3]],
    material_name="S235",
    section_name="IPE 200",
)
```

### Performance: bulk operations

Use `begin_edit()` when creating many objects at once. It wraps the operations
in a single COM transaction, giving a 10–100× speed improvement for large models:

```python
with app.model.begin_edit():
    for i, (x, y, z) in enumerate(node_coords, start=1):
        app.model.geometry.add_node([[i, x, y, z]])
    app.model.geometry.add_member(members_array, section_name="CHS 88.9x4")
```

### Shells and cladding

```python
# Shell panel
app.model.geometry.add_shell_by_contour(
    points=[[1, 0,0,0], [2, 5,0,0], [3, 5,5,0], [4, 0,5,0]],
    thickness=0.2,
    thickness_name="200mm",
    material_name="C25/30",
)

# Cladding (load-distributing surface, not meshed)
app.model.geometry.add_cladding(
    points=[[1, 0,0,3], [2, 5,0,3], [3, 5,5,3], [4, 0,5,3]],
    load_distribution="Two-way",
)
```

### Supports

```python
# Define a named support type
app.model.supports.define_nodal_support("Pinned", ux=1, uy=1, uz=1)
app.model.supports.define_nodal_support("Fixed", ux=1, uy=1, uz=1, rx=1, ry=1, rz=1)
app.model.supports.define_nodal_support("RollerZ", uz=1)

# Apply to nodes
app.model.supports.apply_node_support([1, 2], "Pinned")
```

## Loads

```python
# Create load cases
app.loads.cases.add_loadcase(
    "Self-weight", CaseNature.PERMANENT, CaseAnalizeType.STATIC_LINEAR, number=1
)
app.loads.cases.add_loadcase(
    "Live load", CaseNature.EXPLOITATION, CaseAnalizeType.STATIC_LINEAR, number=2
)

# Apply loads
app.loads.load.add_self_weight("Self-weight", objects="all")
app.loads.load.add_uniform_load("Live load", objects="all", loads=[0, 0, -5000, 0, 0, 0])

# Create a combination
app.loads.combinations.add_combination(
    comb_number=3,
    comb_name="ULS 1",
    label="3",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    factors=[(1, 1.35), (2, 1.5)],
    case_nature=CaseNature.PERMANENT,
)
```

## Calculating and reading results

```python
# Run analysis
app.calculate()

# Read bar forces at midspan
forces = app.query.results.get_forces(bar_number=1, case_number=2)
print(f"My = {forces.my:.1f} Nm")

# Read node list
nodes = app.query.nodes.get_all_in_list()
```

## Accessing the raw COM API

If you need functionality not yet wrapped, access the underlying COM objects directly:

```python
app._raw   # RobotApplication COM object → access app._raw.Project, etc.
app._rbt   # RobotOM module → access all COM interfaces and enums
```
