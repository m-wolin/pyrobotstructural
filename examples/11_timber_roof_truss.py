"""
Timber Roof Truss — Parametric 2D Frame
========================================

Geometry
--------
Symmetric Pratt-style truss in the XZ plane (Y = 0 for all nodes):

  Ridge ──────────────────────────────
       / \\ /|\\ / |/ \\  |  / |\\ /
      /   X  | X   |   X  | X   \\
     /  /  \\ | / \\ | / \\ |/  \\  \\
  ●━━━━━━━━●━━━━━━━━●━━━━━━━━●━━━━━━━━●
  ↑ Pinned                          Roller ↑

Diagonal pattern (Pratt): end panels are already closed triangles;
interior panels each get one diagonal:
  • Left  half panels: diagonal from bottom-right corner → top-left corner
  • Right half panels: diagonal from bottom-left corner → top-right corner
Under dominant gravity loads these diagonals are in tension.

Member groups:
  • Bottom chord (tie beam)  — horizontal, C24 timber, BC_140x220
  • Top chord   (rafters)    — sloped, C24 timber, TC_120x200
  • Verticals   (posts)      — plumb, C24 timber, V_100x160
  • Diagonals                — C24 timber, D_80x140

Load cases
----------
  1  Self-weight    (SW)   — structure self-weight in -Z
  2  Permanent load (PL)   — roofing, ceiling, etc. on top chord in -Z
  3  Live load      (LL)   — maintenance load on top chord in -Z
  4  Snow           (S)    — snow on horizontal projection of top chord
  5  Wind_W         (Ww)   — wind from left (windward left rafter, suction right)
  6  Wind_E         (We)   — wind from right (windward right rafter, suction left)

Wind model (EN 1991-1-4 simplified, duopitch roof):
  Force per unit length on rafter = −Cpe · q_wind · tributary · n̂_outward
    Left rafter outward normal  n̂_L = (−sin α, 0,  cos α)
    Right rafter outward normal n̂_R = ( sin α, 0,  cos α)
  Cpe windward = +0.8 (pressure), Cpe leeward = −0.4 (suction)

ULS/SLS combinations (EN 1990 Eq. 6.10):
  ULS-1: 1.35·G + 1.5·LL
  ULS-2: 1.35·G + 1.5·S  + 0.9·LL
  ULS-3: 1.35·G + 1.5·Ww + 0.9·S
  ULS-4: 1.35·G + 1.5·We + 0.9·S
  SLS-1: 1.0·G  + 1.0·LL
  SLS-2: 1.0·G  + 1.0·S

NOTE: Open a blank Robot model (Frame 2D Design) before running.
      The built-in "Pinned" support label must exist in the model.
"""

import math
import pyrobotstructural
from pyrobotstructural.enums import CaseNature, CaseAnalizeType, CombinationType

# ===========================================================================
# USER PARAMETERS  ← adjust to suit your project
# ===========================================================================

SPAN = 12.0  # Truss span [m]
N_PANELS = 4  # Number of panels along span (must be even for symmetry)
SLOPE_DEG = 20.0  # Roof slope [degrees]
TRIBUTARY = 5.0  # Spacing between trusses (tributary width) [m]

# Solid rectangular timber cross-sections: (section_name, height_mm, width_mm)
# Sizes proposed for C24 timber, 12 m span, 5 m spacing.
# Adjust based on verification results.
SEC_TOP_CHORD = ("TC_120x200", 200, 120)  # rafter: 120 mm wide × 200 mm deep
SEC_BOT_CHORD = ("BC_140x220", 220, 140)  # tie beam: 140 mm wide × 220 mm deep
SEC_VERTICAL = ("V_100x160", 160, 100)  # post:    100 mm wide × 160 mm deep
SEC_DIAGONAL = ("D_80x140", 140, 80)  # diagonal: 80 mm wide × 140 mm deep

MATERIAL = "C24"

# Characteristic load intensities
PERM_kPa = 1.0  # Permanent load (roofing, insulation, ceiling) [kN/m²]
LIVE_kPa = 0.4  # Live/maintenance load [kN/m²]
SNOW_kPa = 1.5  # Snow load on horizontal projection [kN/m²]
WIND_kPa = 0.6  # Reference wind pressure [kN/m²]

DLL_PATH = (
    r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026"
    r"\Exe\Interop.RobotOM.dll"
)

# ===========================================================================
# DERIVED GEOMETRY
# ===========================================================================

slope_rad = math.radians(SLOPE_DEG)
sin_a = math.sin(slope_rad)
cos_a = math.cos(slope_rad)
dx = SPAN / N_PANELS  # panel length along bottom chord [m]
h_ridge = (SPAN / 2) * math.tan(slope_rad)  # ridge height [m]


def top_height(x: float) -> float:
    """Top-chord elevation at horizontal position x from left support."""
    return (SPAN / 2 - abs(x - SPAN / 2)) * math.tan(slope_rad)


# --- Node coordinates ---
node_data = []
_nid = 1

bottom_ids: list[int] = []  # node IDs along bottom chord (left → right)
for i in range(N_PANELS + 1):
    node_data.append([_nid, i * dx, 0.0, 0.0])
    bottom_ids.append(_nid)
    _nid += 1

top_ids: list[int] = [
    bottom_ids[0]
]  # top-chord node IDs; ends shared with bottom chord
for i in range(1, N_PANELS):
    x = i * dx
    node_data.append([_nid, x, 0.0, top_height(x)])
    top_ids.append(_nid)
    _nid += 1
top_ids.append(bottom_ids[-1])

# --- Member topology ---
_mid = 1

bot_chord_data: list[list[int]] = []
top_chord_data: list[list[int]] = []
vertical_data: list[list[int]] = []
diagonal_data: list[list[int]] = []

bot_chord_ids: list[int] = []
top_chord_ids: list[int] = []
top_left_ids: list[int] = []  # left rafter members (for wind loads)
top_right_ids: list[int] = []  # right rafter members
vertical_ids: list[int] = []
diagonal_ids: list[int] = []

half = N_PANELS // 2

for i in range(N_PANELS):
    bot_chord_data.append([_mid, bottom_ids[i], bottom_ids[i + 1]])
    bot_chord_ids.append(_mid)
    _mid += 1

for i in range(N_PANELS):
    top_chord_data.append([_mid, top_ids[i], top_ids[i + 1]])
    top_chord_ids.append(_mid)
    (top_left_ids if i < half else top_right_ids).append(_mid)
    _mid += 1

for i in range(1, N_PANELS):
    if bottom_ids[i] != top_ids[i]:  # skip if nodes coincide (at supports)
        vertical_data.append([_mid, bottom_ids[i], top_ids[i]])
        vertical_ids.append(_mid)
        _mid += 1

# Pratt diagonals — one per interior panel (panels 1 … N_PANELS-2).
# End panels (0 and N_PANELS-1) are already closed triangles formed by the
# top chord + vertical + bottom chord; no additional diagonal is needed there.
#
# Left  half (i < half): bottom-right corner → top-left corner of the panel
#   → diagonal slopes toward the support (in tension under gravity)
# Right half (i ≥ half): bottom-left corner → top-right corner of the panel
#   → mirror image (symmetric)
for i in range(1, N_PANELS - 1):
    if i < half:
        n_start, n_end = bottom_ids[i + 1], top_ids[i]
    else:
        n_start, n_end = bottom_ids[i], top_ids[i + 1]
    diagonal_data.append([_mid, n_start, n_end])
    diagonal_ids.append(_mid)
    _mid += 1


def _ids(lst: list[int]) -> str:
    """Convert a list of IDs to the space-separated string Robot expects."""
    return " ".join(str(n) for n in lst)


# ===========================================================================
# INITIALIZE
# ===========================================================================

pyrobotstructural.initialize(DLL_PATH)
app = pyrobotstructural.RobotApp()
app.model.management.clear()

# ===========================================================================
# SECTIONS  (must exist before add_member references them)
# ===========================================================================

for sec_name, height_mm, width_mm in (
    SEC_TOP_CHORD,
    SEC_BOT_CHORD,
    SEC_VERTICAL,
    SEC_DIAGONAL,
):
    app.model.sections.create_rect_section(
        name=sec_name,
        height=height_mm,
        width=width_mm,
        material=MATERIAL,
    )

# ===========================================================================
# SUPPORT LABELS  (must be defined outside begin_edit)
# ===========================================================================

# Roller: free in X (horizontal), fixed in Y (out-of-plane) and Z (vertical)
app.model.supports.define_nodal_support(
    name="Roller", ux=0, uy=1, uz=1, rx=0, ry=0, rz=0
)

# ===========================================================================
# GEOMETRY  (batched into a single multi-operation flush)
# ===========================================================================

with app.model.begin_edit():
    app.model.geometry.add_node(node_data)

    # Each member group uses its own section directly
    app.model.geometry.add_member(
        top_chord_data, section_name=SEC_TOP_CHORD[0], material_name=MATERIAL
    )
    app.model.geometry.add_member(
        bot_chord_data, section_name=SEC_BOT_CHORD[0], material_name=MATERIAL
    )
    if vertical_data:
        app.model.geometry.add_member(
            vertical_data, section_name=SEC_VERTICAL[0], material_name=MATERIAL
        )
    if diagonal_data:
        app.model.geometry.add_member(
            diagonal_data, section_name=SEC_DIAGONAL[0], material_name=MATERIAL
        )

    # Supports: pinned left, roller right
    app.model.supports.apply_node_support(
        node_number=bottom_ids[0], support_name="Pinned"
    )
    app.model.supports.apply_node_support(
        node_number=bottom_ids[-1], support_name="Roller"
    )

# ===========================================================================
# LOAD CASES
# ===========================================================================

app.loads.cases.add_loadcase(
    name="Self-weight",
    nature=CaseNature.PERMANENT,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=1,
    label="SW",
)
app.loads.cases.add_loadcase(
    name="Permanent load",
    nature=CaseNature.PERMANENT,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=2,
    label="PL",
)
app.loads.cases.add_loadcase(
    name="Live load",
    nature=CaseNature.EXPLOITATION,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=3,
    label="LL",
)
app.loads.cases.add_loadcase(
    name="Snow",
    nature=CaseNature.SNOW,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=4,
    label="S",
)
app.loads.cases.add_loadcase(
    name="Wind_W",
    nature=CaseNature.WIND,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=5,
    label="Ww",
)
app.loads.cases.add_loadcase(
    name="Wind_E",
    nature=CaseNature.WIND,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
    number=6,
    label="We",
)

# ===========================================================================
# LOADS
# ===========================================================================

# Line intensities [N/m] = pressure [kN/m²] × 1 000 × tributary [m]
q_perm = PERM_kPa * 1_000 * TRIBUTARY
q_live = LIVE_kPa * 1_000 * TRIBUTARY
q_snow = SNOW_kPa * 1_000 * TRIBUTARY
q_wind = WIND_kPa * 1_000 * TRIBUTARY

all_top = _ids(top_chord_ids)
left_top = _ids(top_left_ids)
right_top = _ids(top_right_ids)

# 1 — Self-weight (structure dead load, -Z direction)
app.loads.load.add_self_weight(
    case_name="Self-weight", objects="all", factors=[0, 0, -1]
)

# 2 — Permanent load: vertical uniform load on top chord (roofing, ceiling, etc.)
app.loads.load.add_uniform_load(
    case_name="Permanent load",
    objects=all_top,
    loads=[0, 0, -q_perm, 0, 0, 0],
)

# 3 — Live load: vertical uniform load on top chord (maintenance)
app.loads.load.add_uniform_load(
    case_name="Live load",
    objects=all_top,
    loads=[0, 0, -q_live, 0, 0, 0],
)

# 4 — Snow: vertical projected load on top chord (acts on horizontal projection)
app.loads.load.add_uniform_load(
    case_name="Snow",
    objects=all_top,
    loads=[0, 0, -q_snow, 0, 0, 0],
    projected=1,
)

# 5 — Wind_W (wind from left, +X direction)
#
# Force per unit member length = −Cpe · q_wind · n̂_outward
#   Left rafter  n̂_L = (−sin α, 0,  cos α)  →  Fx =  Cpe · q · sin α,  Fz = −Cpe · q · cos α
#   Right rafter n̂_R = ( sin α, 0,  cos α)  →  Fx = −Cpe · q · sin α,  Fz = −Cpe · q · cos α

Cpe_wind = 0.8  # windward pressure coefficient (positive = into surface)
Cpe_lee = -0.4  # leeward suction coefficient  (negative = away from surface)

app.loads.load.add_uniform_load(
    case_name="Wind_W",
    objects=left_top,
    loads=[
        Cpe_wind * q_wind * sin_a,  # Fx  [N/m]  rightward pressure component
        0,
        -Cpe_wind * q_wind * cos_a,  # Fz  [N/m]  downward pressure component
        0,
        0,
        0,
    ],
)
app.loads.load.add_uniform_load(
    case_name="Wind_W",
    objects=right_top,
    loads=[
        -Cpe_lee * q_wind * sin_a,  # Fx  [N/m]  rightward (leeward suction)
        0,
        -Cpe_lee * q_wind * cos_a,  # Fz  [N/m]  upward (uplift / suction)
        0,
        0,
        0,
    ],
)

# 6 — Wind_E (wind from right, −X direction) — mirror of Wind_W
app.loads.load.add_uniform_load(
    case_name="Wind_E",
    objects=right_top,
    loads=[
        -Cpe_wind * q_wind * sin_a,  # Fx  [N/m]  leftward pressure component
        0,
        -Cpe_wind * q_wind * cos_a,  # Fz  [N/m]  downward pressure component
        0,
        0,
        0,
    ],
)
app.loads.load.add_uniform_load(
    case_name="Wind_E",
    objects=left_top,
    loads=[
        Cpe_lee * q_wind * sin_a,  # Fx  [N/m]  leftward (leeward suction)
        0,
        -Cpe_lee * q_wind * cos_a,  # Fz  [N/m]  upward (uplift / suction)
        0,
        0,
        0,
    ],
)

# ===========================================================================
# COMBINATIONS  (EN 1990 Eq. 6.10 — ultimate and serviceability)
# G = SW (1) + PL (2),  variable actions: LL (3), S (4), Ww (5), We (6)
# ===========================================================================

app.loads.combinations.add_combination(
    comb_number=7,
    comb_name="ULS-1 (LL dom.)",
    label="ULS1",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.EXPLOITATION,
    factors=[(1, 1.35), (2, 1.35), (3, 1.5)],
)
app.loads.combinations.add_combination(
    comb_number=8,
    comb_name="ULS-2 (Snow dom.)",
    label="ULS2",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.SNOW,
    factors=[(1, 1.35), (2, 1.35), (4, 1.5), (3, 0.9)],
)
app.loads.combinations.add_combination(
    comb_number=9,
    comb_name="ULS-3 (Wind_W dom.)",
    label="ULS3",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.WIND,
    factors=[(1, 1.35), (2, 1.35), (5, 1.5), (4, 0.9)],
)
app.loads.combinations.add_combination(
    comb_number=10,
    comb_name="ULS-4 (Wind_E dom.)",
    label="ULS4",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.WIND,
    factors=[(1, 1.35), (2, 1.35), (6, 1.5), (4, 0.9)],
)
app.loads.combinations.add_combination(
    comb_number=11,
    comb_name="SLS-1 (LL char.)",
    label="SLS1",
    comb_type=CombinationType.SLS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.EXPLOITATION,
    factors=[(1, 1.0), (2, 1.0), (3, 1.0)],
)
app.loads.combinations.add_combination(
    comb_number=12,
    comb_name="SLS-2 (Snow char.)",
    label="SLS2",
    comb_type=CombinationType.SLS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.SNOW,
    factors=[(1, 1.0), (2, 1.0), (4, 1.0)],
)

# ===========================================================================
# CALCULATE
# ===========================================================================

app.calculate(ignore_warnings=True)

# ===========================================================================
# SUMMARY
# ===========================================================================

total_members = (
    len(top_chord_ids) + len(bot_chord_ids) + len(vertical_ids) + len(diagonal_ids)
)
print("Timber roof truss generated and calculated successfully.")
print(f"  Span           : {SPAN} m")
print(f"  Slope          : {SLOPE_DEG}°  (ridge height {h_ridge:.3f} m)")
print(f"  Panels         : {N_PANELS}  (panel width {dx:.3f} m)")
print(f"  Tributary width: {TRIBUTARY} m")
print(f"  Nodes          : {len(node_data)}")
print(
    f"  Members        : {total_members}"
    f"  (top chord: {len(top_chord_ids)}, bottom chord: {len(bot_chord_ids)},"
    f" verticals: {len(vertical_ids)}, diagonals: {len(diagonal_ids)})"
)
print(f"  Sections:")
print(
    f"    Top chord  — {SEC_TOP_CHORD[0]}  ({SEC_TOP_CHORD[2]} × {SEC_TOP_CHORD[1]} mm, {MATERIAL})"
)
print(
    f"    Bot chord  — {SEC_BOT_CHORD[0]}  ({SEC_BOT_CHORD[2]} × {SEC_BOT_CHORD[1]} mm, {MATERIAL})"
)
print(
    f"    Verticals  — {SEC_VERTICAL[0]}   ({SEC_VERTICAL[2]} × {SEC_VERTICAL[1]} mm, {MATERIAL})"
)
print(
    f"    Diagonals  — {SEC_DIAGONAL[0]}   ({SEC_DIAGONAL[2]} × {SEC_DIAGONAL[1]} mm, {MATERIAL})"
)
print(f"  Load intensities (line loads after tributary {TRIBUTARY} m):")
print(f"    Permanent  : {q_perm / 1000:.1f} kN/m")
print(f"    Live       : {q_live / 1000:.1f} kN/m")
print(f"    Snow       : {q_snow / 1000:.1f} kN/m  (projected)")
print(
    f"    Wind ref.  : {q_wind / 1000:.1f} kN/m  (Cpe_wind={Cpe_wind}, Cpe_lee={Cpe_lee})"
)
