"""
Parametric triangular lattice tower.

Footprint: equilateral triangle centered at (0, 0, 0), one vertex pointing +Y.
The circumradius of the cross-section tapers inward with height and is capped at
the upper_segment_width once reached.

Each segment is divided at mid-height by intermediate leg nodes. All three faces
of the tower carry X-bracing in each half-panel (lower X and upper X per segment).

Parameters
----------
base_width          : Side length of the equilateral triangle at z=0 [m]
segment_height      : Height of one segment [m]
number_of_segments  : Total number of segments
upper_segment_width : Minimum side length — maintained once taper reaches it [m]
taper_slope         : Circumradius reduction per unit height [m/m]
                      (5% means each leg moves 5 cm inward per 1 m of height)

Members
-------
Legs and horizontals : MAIN_SECTION  (CHS101.6x6)
Cross-bracing        : BRACING_SECTION (L100x65x8)

NOTE: You need to open a blank Robot model, go for Shell Design or Frame 3D Design structure type.
      "Pinned" support label must exist in the model (Robot built-in default).
"""

import math
import pyrobotstructural

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
base_width = 6.1  # Side length of base triangle [m]
segment_height = 6.0  # Height of each segment [m]
number_of_segments = 7  # Total number of segments
upper_segment_width = 2.5  # Minimum (upper) side length [m]
taper_slope = 0.05  # Circumradius reduction per unit height [m/m]

MAIN_SECTION = "CHS 114.3x6"
BRACING_SECTION = "CAI 90x70x8"
MATERIAL = "S235"

# ---------------------------------------------------------------------------
# Initialize
# ---------------------------------------------------------------------------
dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"
pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()
app.model.management.clear()

# ---------------------------------------------------------------------------
# Load sections from database
# ---------------------------------------------------------------------------
app.model.sections.add_database("CORUS")
app.model.sections.load_from_database(database_name="CORUS", section_name=MAIN_SECTION)

app.model.sections.load_from_database(
    database_name="EURO", section_name=BRACING_SECTION
)

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
# Equilateral triangle: circumradius R = side_length / sqrt(3)
base_radius = base_width / math.sqrt(3)
upper_radius = upper_segment_width / math.sqrt(3)

# Leg angles: vertex at +Y, then 120° and 240° further around
LEG_ANGLES = [math.radians(a) for a in (90, 210, 330)]


def radius_at(z: float) -> float:
    """Circumradius of the triangular cross-section at height z."""
    return max(base_radius - taper_slope * z, upper_radius)


def leg_xy(z: float, leg: int) -> tuple[float, float]:
    r = radius_at(z)
    return r * math.cos(LEG_ANGLES[leg]), r * math.sin(LEG_ANGLES[leg])


def node_id(level: int, leg: int) -> int:
    """1-based node ID. level: 0 … 2*N (full and mid), leg: 0, 1, 2."""
    return level * 3 + leg + 1


# Total levels: bottom + one mid + one top per segment, shared between segments
# Pattern: [full, mid, full, mid, ..., full]  →  2*N + 1 levels
n_levels = 2 * number_of_segments + 1

# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------
node_data = []
for level in range(n_levels):
    z = level * segment_height / 2
    for leg in range(3):
        x, y = leg_xy(z, leg)
        node_data.append([node_id(level, leg), x, y, z])

app.model.geometry.add_node(node_data)

# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------
member_id = 1
leg_members = []
ring_members = []
bracing_members = []

# Leg members — connect each level to the next along the same leg
for level in range(n_levels - 1):
    for leg in range(3):
        leg_members.append([member_id, node_id(level, leg), node_id(level + 1, leg)])
        member_id += 1

# Horizontal ring members — connect the three legs at every level (full and mid)
for level in range(n_levels):
    for leg in range(3):
        ring_members.append(
            [member_id, node_id(level, leg), node_id(level, (leg + 1) % 3)]
        )
        member_id += 1

# Cross-bracing — X pattern in each half-panel on all three faces
# For each segment:
#   lower half:  leg_a[bot] → leg_b[mid]  and  leg_b[bot] → leg_a[mid]
#   upper half:  leg_a[mid] → leg_b[top]  and  leg_b[mid] → leg_a[top]
face_pairs = [(0, 1), (1, 2), (2, 0)]

for seg in range(number_of_segments):
    level_bot = 2 * seg
    level_mid = 2 * seg + 1
    level_top = 2 * seg + 2

    for a, b in face_pairs:
        # Lower X
        bracing_members.append(
            [member_id, node_id(level_bot, a), node_id(level_mid, b)]
        )
        member_id += 1
        bracing_members.append(
            [member_id, node_id(level_bot, b), node_id(level_mid, a)]
        )
        member_id += 1
        # Upper X
        bracing_members.append(
            [member_id, node_id(level_mid, a), node_id(level_top, b)]
        )
        member_id += 1
        bracing_members.append(
            [member_id, node_id(level_mid, b), node_id(level_top, a)]
        )
        member_id += 1

app.model.geometry.add_member(
    leg_members, section_name=MAIN_SECTION, material_name=MATERIAL
)
app.model.geometry.add_member(
    ring_members, section_name=MAIN_SECTION, material_name=MATERIAL
)
app.model.geometry.add_member(
    bracing_members, section_name=BRACING_SECTION, material_name=MATERIAL
)

# ---------------------------------------------------------------------------
# Supports — Pinned at all three base nodes
# ---------------------------------------------------------------------------
base_nodes = [node_id(0, leg) for leg in range(3)]
app.model.supports.apply_node_support(node_number=base_nodes, support_name="Pinned")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
total_members = len(leg_members) + len(ring_members) + len(bracing_members)
print("Tower generated successfully.")
print(f"  Segments     : {number_of_segments}")
print(f"  Total height : {number_of_segments * segment_height} m")
print(f"  Base width   : {base_width} m  (circumradius {base_radius:.3f} m)")
print(
    f"  Top width    : {radius_at(number_of_segments * segment_height) * math.sqrt(3):.3f} m"
)
print(f"  Nodes        : {len(node_data)}")
print(
    f"  Members      : {total_members}  "
    f"(legs: {len(leg_members)}, rings: {len(ring_members)}, bracing: {len(bracing_members)})"
)
