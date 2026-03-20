"""
Simple beam example using the pyrobotstructural wrapper.

The workflow:
  - Creates geometry: 4 nodes, 3 bars (IPE 100)
  - Pinned support at node 1, Roller support at nodes 2-4
  - Self-weight (permanent) + live uniform load (exploitation)
  - ULS 1 combination (1.35 SW + 1.5 LL)
  - Calculate and display bending moment My

Performance notes:
  - Geometry and support creation are wrapped in ``app.model.begin_edit()`` to
    batch all COM writes into a single multi-operation flush.
  - Load records share a case object via the internal case cache, so each
    ``add_*`` load call costs a dict lookup instead of a full COM scan.

NOTE: You need to open a blank Robot model, go for Frame 2D Design or Frame 3D Design structure type.
      "Pinned" support label must exist in the model (Robot built-in default).
"""

import pyrobotstructural
from pyrobotstructural.enums import CaseNature, CaseAnalizeType, CombinationType

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()

# Clear any previous model content
app.model.management.clear()

# Custom roller support must be defined before the multi-operation block
# because label creation is not batched.
app.model.supports.define_nodal_support(
    name="Roller", ux=0, uy=1, uz=1, rx=0, ry=0, rz=0
)

# --- Geometry + supports — batched into a single multi-operation flush ---
with app.model.begin_edit():
    app.model.geometry.add_node(
        [
            [1, 0, 0, 0],
            [2, 3, 0, 0],
            [3, 6, 0, 0],
            [4, 9, 0, 0],
        ]
    )
    app.model.geometry.add_member(
        [[1, 1, 2], [2, 2, 3], [3, 3, 4]],
        section_name="IPE 100",
    )
    # Pinned at node 1 (predefined label assumed to exist)
    app.model.supports.apply_node_support(node_number=1, support_name="Pinned")
    app.model.supports.apply_node_support(node_number=[2, 3, 4], support_name="Roller")

# --- Load cases ---
app.loads.cases.add_loadcase(
    name="Self-weight",
    nature=CaseNature.PERMANENT,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=1,
)

app.loads.cases.add_loadcase(
    name="Live load",
    nature=CaseNature.EXPLOITATION,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=2,
)

# --- Loads ---
# Self-weight acting in -Z direction
app.loads.load.add_self_weight(
    case_name="Self-weight",
    objects="all",
    factors=[0, 0, -1],
)

# Uniform live load: -500 N/m in Z direction
app.loads.load.add_uniform_load(
    case_name="Live load",
    objects="all",
    loads=[0, 0, -500, 0, 0, 0],
)

# --- Combination ---
app.loads.combinations.add_combination(
    comb_number=3,
    comb_name="ULS 1",
    label="3",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.PERMANENT,
    factors=[(1, 1.35), (2, 1.5)],
)

# --- Calculate ---
app.calculate(ignore_warnings=True)

# --- Display bending moment My ---
app.view.view.display_member_forces(
    Fx=False, Fy=False, Fz=False, Mx=False, My=True, Mz=False, labels=True, scale=1
)

# --- Save screenshot ---
model_path = app.query.model.get_model_path()
app.view.screenshots.save_screenshot(name="Moments-My", dir_path=model_path)

print("Done.")
