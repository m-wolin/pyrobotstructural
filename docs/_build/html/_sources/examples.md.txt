# Examples

The `examples/` directory contains runnable scripts that demonstrate the library
from simple to advanced use cases.

## 01 — Initialize

**File:** `examples/01_initialize.py`

Connects to Robot and verifies the connection by adding a single node.
The simplest possible starting point.

## 02 — Build geometry

**File:** `examples/02_build_geometry.py`

Demonstrates adding nodes, bars (members), shell panels, and cladding surfaces.
Shows how to use `begin_edit()` to batch many geometry operations into a single
COM transaction for large performance gains.

## 03 — Loads

**File:** `examples/03_loads.py`

Creates load cases (permanent and exploitation natures), applies several load
types (self-weight, uniform member loads, panel loads), and creates ULS and SLS
combinations with load factors.

## 04 — View control

**File:** `examples/04_view_control.py`

Interactive demonstration of the viewport API: zoom, pan, rotate, toggling
display annotations (node numbers, section shapes, local axes, supports), and
switching between results visualisations (forces, displacements, reactions,
stresses, utilisations).

## 05 — Query model data

**File:** `examples/05_query.py`

Read-only access to model objects: lists all nodes, bars, load cases, and
combinations from a calculated Robot model.

## 05a — Query bar results

**File:** `examples/05a_query_member_results.py`

Queries bar member analysis results: internal forces at a point, forces at
multiple points along the bar, maximum deflection, cross-section stresses, and
stress envelopes.

## 05b — Query shell results

**File:** `examples/05b_query_shell_results.py`

Queries shell finite element results: in-plane forces (Nxx, Nyy, Mxx, Myy,
Qxx, Qyy) and stresses (Sxx, Syy, von Mises) at the mid, top, and bottom
through-thickness layers.

## 06 — Full beam example

**File:** `examples/06_beam_example.py`

Complete end-to-end workflow on a simple 4-node beam: pinned and roller
supports, self-weight and live load cases, a ULS combination, calculation,
and visualisation of the My bending moment diagram with a screenshot.

## 07 — Support types

**File:** `examples/07_supports.py`

Advanced support definitions covering all available types:

- Rigid (pinned, fixed, roller)
- Elastic translational and rotational springs
- One-directional (compression-only or tension-only)
- Combined elastic + unilateral
- Skewed supports (local-axis orientation via alpha/beta/gamma)

## 08 — Lattice tower

**File:** `examples/08_lattice_tower.py`

Parametric triangular lattice tower with ~160 nodes and ~300 members.
Demonstrates the performance benefit of `begin_edit()` for bulk geometry
creation, section database loading, and complex member topologies.

## 09 — Cladding local coordinate systems

**File:** `examples/09_cladding_local_cs.py`

Six cladding panel configurations showing `dir_x` for explicit span direction
control and `flip_z` for surface normal reversal.  Useful for correctly
directing one-way cladding loads.

## 10 — Custom sections

**File:** `examples/10_sections.py`

Creates non-standard cross-sections programmatically:

- Circular hollow sections (CHS / tubes)
- Solid rectangular sections
- Rectangular hollow sections (RHS)

Also demonstrates assigning different sections to individual bars after creation.
