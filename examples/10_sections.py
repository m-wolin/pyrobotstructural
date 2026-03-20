"""
Example: custom tube (CHS) and rectangular (solid / RHS) sections.

Three custom sections are created and applied to bars of a simple portal frame:

  Bar 1  (column left)   → CHS 168.3x10  (tube section, D=168.3 mm, t=10 mm)
  Bar 2  (column right)  → CHS 168.3x10
  Bar 3  (beam)          → RECT 200x100  (solid rectangular section)
  Bar 4  (diagonal)      → RHS 150x100x6 (hollow rectangular section)

Unit conventions
----------------
create_tube_section  : diameter and thickness in **meters**
create_rect_section  : height, width and thickness in **millimeters**

NOTE: Open a blank Robot model (Frame 3D Design) before running.
      A "Fixed" support label must exist (Robot built-in default).
"""

import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()
app.model.management.clear()

# ---------------------------------------------------------------------------
# Geometry — simple portal frame with a diagonal brace
# ---------------------------------------------------------------------------
#
#   3 -------- 4
#   |  \       |
#   |    \     |
#   1          2
#
nodes = [
    [1, 0.0, 0.0, 0.0],  # base left
    [2, 4.0, 0.0, 0.0],  # base right
    [3, 0.0, 0.0, 3.0],  # top left
    [4, 4.0, 0.0, 3.0],  # top right
]

bars = [
    [1, 1, 3],  # column left
    [2, 2, 4],  # column right
    [3, 3, 4],  # beam
    [4, 1, 4],  # diagonal brace
]

with app.model.begin_edit():
    app.model.geometry.add_node(nodes)
    # Temporary section; will be overwritten per bar below
    app.model.geometry.add_member(bars, material_name="S235", section_name="IPE 100")
    app.model.supports.apply_node_support(node_number=[1, 2], support_name="Fixed")

# ---------------------------------------------------------------------------
# Custom sections
# ---------------------------------------------------------------------------

# CHS 168.3x10 — diameter 168.3 mm = 0.1683 m, wall thickness 10 mm = 0.010 m
app.model.sections.create_tube_section(
    name="CHS 168.3x10",
    diameter=0.1683,
    thickness=0.010,
    material="S235",
)

# Solid rectangle 200 mm (H) × 100 mm (W)
app.model.sections.create_rect_section(
    name="RECT 200x100",
    height=200,
    width=100,
    material="S235",
)

# Hollow RHS 150 mm (H) × 100 mm (W), wall thickness 6 mm
app.model.sections.create_rect_section(
    name="RHS 150x100x6",
    height=150,
    width=100,
    thickness=6,
    material="S235",
)

# ---------------------------------------------------------------------------
# Assign sections to bars
# ---------------------------------------------------------------------------
app.model.sections.apply_section_to_bar(1, "CHS 168.3x10")
app.model.sections.apply_section_to_bar(2, "CHS 168.3x10")
app.model.sections.apply_section_to_bar(3, "RECT 200x100")
app.model.sections.apply_section_to_bar(4, "RHS 150x100x6")

print("Sections created and assigned successfully.")
