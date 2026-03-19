"""
View control interactive example — manipulate and display methods.

Demonstrates how to control the Robot Structural Analysis view using
pyrobotstructural. The script is organised in sections; each section
calls input() so you can observe the result in Robot before moving on.

NOTE: Works with any open model — no specific geometry is assumed.

"""

import pyrobotstructural

dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"

pyrobotstructural.initialize(dll_path)


app = pyrobotstructural.RobotApp()
view = app.view.view  # ViewFacade.view → ViewManager

view.restore_default()

# =============================================================================
# 1. MANIPULATE — zoom, pan and rotate the view
# =============================================================================

# Zoom in to 2× the current zoom level.
view.manipulate(zoom_factor=2.0)
input("Zoomed in 2×. Press Enter to zoom back out …")

# Zoom out (factor < 1 moves the camera further away).
view.manipulate(zoom_factor=0.5)
input("Zoomed out. Press Enter to pan the view …")

# Pan: positive pan_up moves the viewport upward, pan_right moves it right.
view.manipulate(zoom_factor=1.0, pan_up=0.5, pan_right=0.5)
input("Panned up and right. Press Enter to rotate …")

# Rotate around X axis by 30 °. Note: rotation only works in 3-D views.
view.manipulate(rotation_x=30.0)
input("Rotated 30 ° around X. Press Enter to rotate back …")

view.manipulate(rotation_x=-30.0)
input("Rotation restored. Press Enter to go to display settings …")

# =============================================================================
# 2. DISPLAY — toggle structural element annotations
# =============================================================================

# Show node and bar numbers.
view.display(node_numbers=True, bar_numbers=True)
input("Node and bar numbers ON. Press Enter to add section shapes …")

# Add section shape rendering and support symbols with labels.
view.display(section_shapes=True, supports=True, with_codes=True)
input("Section shapes and supports with codes ON. Press Enter …")

# Show member local coordinate systems.
view.display(member_lcs=True)
input("Member LCS ON. Press Enter to turn off annotations …")

# Turn everything off to get a clean view.
view.display(
    node_numbers=False,
    bar_numbers=False,
    section_shapes=False,
    supports=False,
    releases=False,
    member_lcs=False,
    panel_lcs=False,
)
input("All annotations OFF. Press Enter to continue to loads display …")

# =============================================================================
# 3. LOADS DISPLAY — show load symbols for different case selections
# =============================================================================

# Show load symbols and values for all simple load cases (default).
view.loads_display(symbols=True, values=True, symbol_size=5)
input("Loads displayed for Simple Cases (default). Press Enter …")

# Show loads for a specific case number.
view.loads_display(symbols=True, values=True, cases="1")
input("Loads displayed for case 1 only. Press Enter …")

# Show loads for all cases (simple + combinations).
view.loads_display(symbols=True, values=True, cases="all")
input("Loads displayed for all cases. Press Enter …")

# Hide load display by disabling symbols.
view.loads_display(symbols=False, values=False)
input("Loads hidden. Press Enter to display member forces …")

# =============================================================================
# 4. RESULTS — member forces, displacements, reactions
#    Requires the model to be analysed before these have an effect.
# =============================================================================

# --- Member forces ---
# Show Mz (bending about local Z) with filled diagram and colour-differentiated
# positive/negative zones. Displayed for all simple load cases.
view.display_member_forces(
    Fx=False,
    Fy=False,
    Fz=True,
    Mx=False,
    My=True,
    Mz=True,
    filling=True,
    pos_neg=True,
    values_type="all",
    labels=True,
    cases="Simple Cases",
)
input("Fz / My / Mz diagrams ON for Simple Cases. Press Enter …")

# Switch to combinations only.
view.display_member_forces(
    Fx=False,
    Fy=False,
    Fz=True,
    Mx=False,
    My=True,
    Mz=True,
    filling=True,
    pos_neg=True,
    values_type="global extremes",
    cases="Combinations",
)
input(
    "Same forces for Combinations, showing global extremes. Press Enter to clear the results…"
)


# --- Reset ---
view.clear_results()

# --- Displacements ---
view.display_displacements(display=True, labels=True, cases="Simple Cases")
input("Deflections shown for Simple Cases. Press Enter to hide …")

view.display_displacements(display=False)
input("Deflections hidden. Press Enter to show reactions …")

# --- Reactions ---
view.display_reactions(Rx=True, Ry=True, Rz=True, cases="Simple Cases")
input("Reactions (Rx, Ry, Rz) shown for Simple Cases. Press Enter to hide …")

view.display_reactions(Rx=False, Ry=False, Rz=False)
input("Reactions hidden. Press Enter to show stresses …")

# --- Stresses ---
view.display_stresses(display=True, s_max=True, labels=True, cases="Simple Cases")
input("Max stress map ON. Press Enter to hide …")

view.display_stresses(display=False)
input("Stresses hidden. Press Enter to show s_max member stresses …")

view.display_member_stresses(display=True, s_max=True, labels=True)
input("Max stress diagram ON. Press Enter to hide …")

view.display_member_stresses(display=False)
input("Stresses hidden. Press Enter to show utilisations …")

# --- Utilisations (requires steel/timber design results) ---
view.display_utilisations(
    display=True, labels=True, thickness_coeff=5, cases="Combinations"
)
input("Utilisation map ON for Combinations. Press Enter to finish …")

view.display_utilisations(display=False)

print("View controlling example complete.")
