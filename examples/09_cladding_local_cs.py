"""
Example: cladding objects with explicit local coordinate system.

Demonstrates how to use the ``dir_x`` and ``flip_z`` parameters of
``add_cladding`` to control the panel's local axes:

1. Default isotropic cladding (Robot auto-computes local axes).
2. One-way cladding spanning in a specific global direction (via ``dir_x``).
3. Cladding with a flipped normal (``flip_z=True``).
4. One-way cladding with a custom diagonal span direction.

Background
----------
A cladding object's local X axis determines the span direction for
one-way load distribution:

* ``"One-way X"`` — load carried along the local X axis
* ``"One-way Y"`` — load carried perpendicular to local X (along local Y)
* ``"Two-way"``   — isotropic; local X direction has no effect

``dir_x`` accepts any non-zero 3-D vector in global coordinates.  The
vector is normalised internally, so only direction matters.

``flip_z=True`` reverses the panel outward normal, effectively swapping
which face is considered the "top" surface.

NOTE: Open a blank Robot model (Frame 3D or Shell Design) before running.
"""

import math
import pyrobotstructural

DLL_PATH = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(DLL_PATH)
app = pyrobotstructural.RobotApp()
app.model.management.clear()

# ---------------------------------------------------------------------------
# Helper: build a rectangular contour in the XY plane at a given Z offset
# ---------------------------------------------------------------------------


def rect_contour(x0, y0, x1, y1, z=0.0):
    """Return a four-point contour list for add_cladding."""
    return [
        [1, x0, y0, z],
        [2, x1, y0, z],
        [3, x1, y1, z],
        [4, x0, y1, z],
    ]


# ---------------------------------------------------------------------------
# 1. Default two-way cladding — Robot auto-computes local X from first edge
# ---------------------------------------------------------------------------

app.model.geometry.add_cladding(
    points=rect_contour(0.0, 0.0, 3.0, 4.0, z=0.0),
    load_distribution="Two-way",
)

# ---------------------------------------------------------------------------
# 2. One-way cladding spanning in global X  (dir_x = (1, 0, 0))
#    Load is distributed along local X, i.e. in the global X direction.
# ---------------------------------------------------------------------------

app.model.geometry.add_cladding(
    points=rect_contour(4.0, 0.0, 7.0, 4.0, z=0.0),
    load_distribution="One-way X",
    dir_x=(1.0, 0.0, 0.0),  # local X = global X
)

# ---------------------------------------------------------------------------
# 3. One-way cladding spanning in global Y  (dir_x = (0, 1, 0))
#    To span in Y we align local X with global Y, then use "One-way X".
# ---------------------------------------------------------------------------

app.model.geometry.add_cladding(
    points=rect_contour(8.0, 0.0, 11.0, 4.0, z=0.0),
    load_distribution="One-way X",
    dir_x=(0.0, 1.0, 0.0),  # local X = global Y → spans in Y direction
)

# ---------------------------------------------------------------------------
# 4. Cladding with flipped normal — load collected from the underside
# ---------------------------------------------------------------------------

app.model.geometry.add_cladding(
    points=rect_contour(0.0, 5.0, 3.0, 9.0, z=0.0),
    load_distribution="Two-way",
    flip_z=True,
)

# ---------------------------------------------------------------------------
# 5. One-way cladding with a 45° diagonal span direction
#    dir_x does not need to be a unit vector — it is normalised internally.
# ---------------------------------------------------------------------------

app.model.geometry.add_cladding(
    points=rect_contour(4.0, 5.0, 7.0, 9.0, z=0.0),
    load_distribution="One-way X",
    dir_x=(1.0, 1.0, 0.0),  # 45° in the XY plane; normalised to (√2/2, √2/2, 0)
)

# ---------------------------------------------------------------------------
# 6. Inclined cladding panel (not in a global plane)
#    The panel is tilted; dir_x points along global X regardless.
# ---------------------------------------------------------------------------

inclined_contour = [
    [1, 0.0, 10.0, 0.0],
    [2, 3.0, 10.0, 0.0],
    [3, 3.0, 13.0, 2.0],  # Z rises
    [4, 0.0, 13.0, 2.0],
]

app.model.geometry.add_cladding(
    points=inclined_contour,
    load_distribution="One-way X",
    dir_x=(1.0, 0.0, 0.0),
)

app.view.view.display(panel_lcs=True)
