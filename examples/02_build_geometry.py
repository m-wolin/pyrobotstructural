"""
This example shows how to define simple geometry objects such as nodes, bars (members), shell and cladding.
It also shows basic support assignment.

NOTE: You need to open a blank Robot model, go for Shell Design or Frame 3D Design structure type.
      "Pinned" support label must exist in the model (Robot built-in default).
"""

import pyrobotstructural

# you can optionally use 'import pyrobotstructural as pyrbt' or similar abbreviation

# --- Initialize ---
dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()

# --- Clear previous model ---
app.model.management.clear()


# --- Define geometry ---
node_data = [
    [1, 0.0, 0.0, 0.0],
    [2, 3.0, 0.0, 0.0],
    [3, 0, 3.0, 0.0],
    [4, 3, 3.0, 0.0],
    [5, 0, 5, 0],
    [6, 3, 5, 0],
    [7, 1.5, 3, 0],
    [8, 1.5, 5, 0],
]

bars = [
    [1, 1, 2],
    [2, 1, 3],
    [3, 2, 4],
    [4, 3, 4],
    [5, 5, 6],
    [6, 7, 8],
    [7, 3, 5],
    [8, 4, 6],
]

# --- Add nodes ---
app.model.geometry.add_node(node_data)

# --- Add bars ---
app.model.geometry.add_member(bars, material_name="S235", section_name="IPE 100")


# --- Geometry for contour ---
contour_for_shell = [
    [1, 0.0, 0.0, 0.0],
    [2, 3.0, 0.0, 0.0],
    [3, 3, 3.0, 0.0],
    [4, 0, 3.0, 0.0],
]

# --- Add slab ---
app.model.geometry.add_shell_by_contour(
    points=contour_for_shell,
    thickness=0.1,
    thickness_name="10cm",
    material_name="C20/25",
)

# --- Add cladding ---
contour_for_cladding = [
    [1, 0, 3.0, 0.0],
    [2, 3, 3.0, 0.0],
    [3, 3, 5, 0],
    [4, 0, 5, 0],
]

app.model.geometry.add_cladding(
    points=contour_for_cladding, load_distribution="Two-way"
)

# --- Add supports ---
app.model.supports.apply_node_support(
    node_number=[1, 2, 3, 4, 5, 6], support_name="Pinned"
)
