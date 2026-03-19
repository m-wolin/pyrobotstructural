"""
This example shows how to define load cases, loads and load combinations.

Performance note: load cases are resolved by name via an internal cache.
The first ``add_*`` call for a given case name scans the COM collection once;
all subsequent calls for the same case cost only a dict lookup.
"""

import pyrobotstructural
from pyrobotstructural.enums import CaseNature, CaseAnalizeType, CombinationType
# you can optionally use 'import pyrobotstructural as pyrbt' or similar abbreviation

# --- Initialize ---
dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()

# --- Clear previous model ---
app.loads.cases.clear()

# --- Define loadcases ---
app.loads.cases.add_loadcase(
    number=1,
    name="Self-weight",
    label="SW",
    nature=CaseNature.PERMANENT,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
)
app.loads.cases.add_loadcase(
    number=2,
    name="Live load",
    label="LL",
    nature=CaseNature.EXPLOITATION,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
)

app.loads.cases.add_loadcase(
    number=3,
    name="Live load 2",
    label="LL2",
    nature=CaseNature.EXPLOITATION,
    analize_type=CaseAnalizeType.STATIC_LINEAR,
)

# --- Define loads ---
app.loads.load.add_self_weight(case_name="Self-weight", objects="all")

app.loads.load.add_uniform_panel_load(
    case_name="Live load", objects="all", loads=[0, 0, -2000]
)

app.loads.load.add_node_load(
    case_name="Live load", objects="1, 6", loads=[0, 0, -3000, 0, 0, 0]
)

app.loads.load.add_uniform_load(
    case_name="Live load 2", objects="6", loads=[1000, 0, -1000, 0, 0, 0]
)

# --- Define combinations ---
app.loads.combinations.add_combination(
    comb_number=100,
    comb_name="ULS 1",
    label="ULS_1",
    comb_type=CombinationType.ULS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.EXPLOITATION,  # Is this needed?
    factors=[(1, 1.35), (2, 1.5), (3, 1.15)],
)


app.loads.combinations.add_combination(
    comb_number=100,
    comb_name="SLS 1",
    label="SLS_1",
    comb_type=CombinationType.SLS,
    case_analize_type=CaseAnalizeType.COMB_LINEAR,
    case_nature=CaseNature.EXPLOITATION,  # Is this needed?
    factors=[(1, 1), (2, 1), (3, 0.6)],
)
