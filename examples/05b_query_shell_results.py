"""
Query shell results — FE forces and stresses for panel elements.

Requires an open and analysed model with panels (shell elements).
All values are in Robot's internal SI units (N, m, Pa, rad).
"""

import pyrobotstructural
from pyrobotstructural.enums import ShellLayer

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)
app = pyrobotstructural.RobotApp()

# Change element_nr to a valid finite element number from your model.
element_nr = 500
case_nr = 1


# =============================================================================
# SHELL (FE) RESULTS
# =============================================================================

print("=" * 60)
print("SHELL FE RESULTS")
print("=" * 60)

for layer_name, layer in [
    ("MID", ShellLayer.MID),
    ("TOP", ShellLayer.TOP),
    ("BOTTOM", ShellLayer.BOTTOM),
]:
    sf = app.query.shell_results.get_forces(
        element_nr,
        case_nr,
        layer=layer,
    )
    print(
        f"\n  Shell forces — element {element_nr}, case {case_nr}, layer={layer_name}:"
    )
    print(
        f"    Nxx={sf.nxx / 1e3:>10.3f} kN/m   Nyy={sf.nyy / 1e3:>10.3f} kN/m   Nxy={sf.nxy / 1e3:>10.3f} kN/m"
    )
    print(
        f"    Mxx={sf.mxx / 1e3:>10.3f} kNm/m  Myy={sf.myy / 1e3:>10.3f} kNm/m  Mxy={sf.mxy / 1e3:>10.3f} kNm/m"
    )
    print(f"    Qxx={sf.qxx / 1e3:>10.3f} kN/m   Qyy={sf.qyy / 1e3:>10.3f} kN/m")

    ss = app.query.shell_results.get_stresses(element_nr, case_nr, layer=layer)
    print(
        f"  Shell stresses — element {element_nr}, case {case_nr}, layer={layer_name}:"
    )
    print(
        f"    Sxx={ss.sxx / 1e6:>10.3f} MPa   Syy={ss.syy / 1e6:>10.3f} MPa   Sxy={ss.sxy / 1e6:>10.3f} MPa"
    )
    print(f"    Txx={ss.txx / 1e6:>10.3f} MPa   Tyy={ss.tyy / 1e6:>10.3f} MPa")
    print(f"    von Mises={ss.mises / 1e6:>10.3f} MPa")

print()
print("Shell results query complete.")
