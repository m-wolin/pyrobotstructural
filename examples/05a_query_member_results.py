"""
Query member results — bar forces, deflections, and stresses.

Requires an open and analysed model with bars.
All values are in Robot's internal SI units (N, m, Pa, rad).
"""

import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)
app = pyrobotstructural.RobotApp()

bar_topo = app.query.bars.get_all_bars_node_numbers()
bar_nr = bar_topo[0][0]  # first bar
case_nr = 1              # adjust to a valid case number in your model

# =============================================================================
# BAR RESULTS
# =============================================================================

print("=" * 60)
print("BAR RESULTS")
print("=" * 60)

# --- Forces at midspan ---
forces = app.query.results.get_forces(bar_nr, case_nr, position=0.5)
print(f"\n  Forces on bar {bar_nr}, case {case_nr}, pos=0.5:")
print(f"    Fx={forces.fx:>12.2f} N   (axial)")
print(f"    Fy={forces.fy:>12.2f} N   (shear local Y)")
print(f"    Fz={forces.fz:>12.2f} N   (shear local Z)")
print(f"    Mx={forces.mx:>12.2f} Nm  (torsion)")
print(f"    My={forces.my:>12.2f} Nm  (bending local Y)")
print(f"    Mz={forces.mz:>12.2f} Nm  (bending local Z)")

# --- Forces at 5 evenly-spaced points ---
force_pts = app.query.results.get_forces_at_points(bar_nr, case_nr, n_points=5)
print(f"\n  Mz envelope on bar {bar_nr}, case {case_nr} (5 points):")
print(f"  {'Point':>7}  {'My [Nm]':>14}")
for idx, f in enumerate(force_pts):
    print(f"  {idx + 1:>7}  {f.my:>14.2f}")

# --- Deflections at midspan ---
defl = app.query.results.get_deflections(bar_nr, case_nr, position=0.5)
print(f"\n  Deflections on bar {bar_nr}, case {case_nr}, pos=0.5:")
print(f"    UX={defl.ux * 1000:>10.4f} mm")
print(f"    UY={defl.uy * 1000:>10.4f} mm")
print(f"    UZ={defl.uz * 1000:>10.4f} mm")
print(f"    RX={defl.rx:>10.6f} rad")
print(f"    RY={defl.ry:>10.6f} rad")
print(f"    RZ={defl.rz:>10.6f} rad")

# --- Maximum deflection at given bar ---
max_defl = app.query.results.get_max_deflection(bar_nr, case_nr)
print(f"\n  Maximum Uz on a bar {bar_nr}, case {case_nr}:")
print(f"  {max_defl.uz * 1000:>12.4f}")

# --- Stresses at midspan ---
stress = app.query.results.get_stresses(bar_nr, case_nr, pos=0.5)
print(f"\n  Stresses on bar {bar_nr}, case {case_nr}, pos=0.5:")
print(f"    Smax   ={stress.smax / 1e6:>10.3f} MPa")
print(f"    Smin   ={stress.smin / 1e6:>10.3f} MPa")
print(f"    Shear Y={stress.shear_y / 1e6:>10.3f} MPa")
print(f"    Shear Z={stress.shear_z / 1e6:>10.3f} MPa")
print(f"    Torsion={stress.torsion / 1e6:>10.3f} MPa")

# --- Stress envelope at 5 points ---
stress_pts = app.query.results.get_stresses_at_points(bar_nr, case_nr, n_points=5)
print(f"\n  Smax envelope on bar {bar_nr}, case {case_nr} (5 points):")
print(f"  {'Point':>7}  {'Smax [MPa]':>12}")
for idx, s in enumerate(stress_pts):
    print(f"  {idx + 1:>7}  {s.smax / 1e6:>12.3f}")

print()
print("Member results query complete.")
