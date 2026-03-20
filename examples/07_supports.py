"""
Example: advanced nodal support definitions.

Demonstrates the full range of nodal support types available through
``define_nodal_support``:

1. Rigid supports (pinned, fixed, roller).
2. Elastic spring supports (translational and rotational springs).
3. One-directional (unilateral) supports — resist load in one direction only,
   e.g. compression-only foundation, tension-only anchor.
4. Combined elastic + one-directional support.
5. Local-axis (skewed) support.

NOTE: Open a blank Robot model (Frame 3D or Shell Design) before running.
"""

import pyrobotstructural

DLL_PATH = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(DLL_PATH)
app = pyrobotstructural.RobotApp()
app.model.management.clear()

# ---------------------------------------------------------------------------
# 1. Rigid supports
# ---------------------------------------------------------------------------

# Pinned: all translations fixed, all rotations free
app.model.supports.define_nodal_support("Pinned", ux=1, uy=1, uz=1)

# Fixed (encastre): all six DOFs restrained
app.model.supports.define_nodal_support("Fixed", ux=1, uy=1, uz=1, rx=1, ry=1, rz=1)

# Roller in Z: only vertical translation fixed
app.model.supports.define_nodal_support("RollerZ", uz=1)

# ---------------------------------------------------------------------------
# 2. Elastic spring supports
# ---------------------------------------------------------------------------

# Translational spring in X only (kN/m)
app.model.supports.define_nodal_support("SpringX_1000", kx=1000.0)

# Winkler-type elastic foundation: springs in all three translations
app.model.supports.define_nodal_support(
    "ElasticFoundation",
    kx=5000.0,   # kN/m
    ky=5000.0,
    kz=10000.0,
)

# Rotational spring about Z (kNm/rad) — semi-rigid column base
app.model.supports.define_nodal_support("SemiRigidBase", uz=1, hz=15000.0)

# ---------------------------------------------------------------------------
# 3. One-directional (unilateral) supports
# ---------------------------------------------------------------------------

# Compression-only vertical support: resists downward movement (negative Z)
# Use "-" to block in the negative direction only.
app.model.supports.define_nodal_support(
    "CompressionOnlyZ",
    one_dir={"uz": "-"},
)

# Tension-only anchor: resists upward pull (positive Z)
app.model.supports.define_nodal_support(
    "TensionOnlyZ",
    one_dir={"uz": "+"},
)

# Multi-DOF unilateral: compression-only Z, friction-like constraint on X+
app.model.supports.define_nodal_support(
    "UnilateralXZ",
    one_dir={"uz": "-", "ux": "+"},
)

# ---------------------------------------------------------------------------
# 4. Combined elastic + one-directional
# ---------------------------------------------------------------------------

# Elastic compression-only spring in Z: spring acts only under compression
app.model.supports.define_nodal_support(
    "ElasticCompressionZ",
    kz=8000.0,
    one_dir={"uz": "-"},
)

# ---------------------------------------------------------------------------
# 5. Skewed (local-axis) support — rotated 45° about global Z
# ---------------------------------------------------------------------------

import math

app.model.supports.define_nodal_support(
    "SkewedPinned45",
    ux=1,
    uy=1,
    uz=1,
    alpha=math.radians(45),  # rotate support axes 45° about Z
)

# ---------------------------------------------------------------------------
# Build a simple four-node frame and apply supports
# ---------------------------------------------------------------------------

with app.model.begin_edit():
    app.model.geometry.add_node([
        [1, 0.0, 0.0, 0.0],
        [2, 5.0, 0.0, 0.0],
        [3, 0.0, 0.0, 3.0],
        [4, 5.0, 0.0, 3.0],
        [5, 2.5, 0.0, 3.0],
    ])
    app.model.geometry.add_member(
        [[1, 1, 3], [2, 2, 4], [3, 3, 5], [4, 5, 4]],
        material_name="S235",
        section_name="IPE 200",
    )

    # Rigid pinned bases
    app.model.supports.apply_node_support(1, "Pinned")
    app.model.supports.apply_node_support(2, "Pinned")

    # Elastic spring under node 5 (mid-span)
    app.model.supports.apply_node_support(5, "SpringX_1000")
