# Examples

The `examples/` directory contains runnable scripts that demonstrate the library
from simple to advanced use cases.

> **Note:** All examples require Autodesk Robot Structural Analysis Professional
> to be running with an open model before execution.

## 01 — Initialize

Connects to Robot and verifies the connection by adding a single node.
The simplest possible starting point.

```{literalinclude} ../examples/01_initialize.py
:language: python
```

## 02 — Build geometry

Demonstrates adding nodes, bars (members), shell panels, and cladding surfaces.
Shows how to use `begin_edit()` to batch many geometry operations into a single
COM transaction for large performance gains.

```{literalinclude} ../examples/02_build_geometry.py
:language: python
```

## 03 — Loads

Creates load cases (permanent and exploitation natures), applies several load
types (self-weight, uniform member loads, panel loads), and creates ULS and SLS
combinations with load factors.

```{literalinclude} ../examples/03_loads.py
:language: python
```

## 04 — View control

Interactive demonstration of the viewport API: zoom, pan, rotate, toggling
display annotations (node numbers, section shapes, local axes, supports), and
switching between results visualisations (forces, displacements, reactions,
stresses, utilisations).

```{literalinclude} ../examples/04_view_control.py
:language: python
```

## 05 — Query model data

Read-only access to model objects: lists all nodes, bars, load cases, and
combinations from a calculated Robot model.

```{literalinclude} ../examples/05_query.py
:language: python
```

## 05a — Query bar results

Queries bar member analysis results: internal forces at a point, forces at
multiple points along the bar, maximum deflection, cross-section stresses, and
stress envelopes.

```{literalinclude} ../examples/05a_query_member_results.py
:language: python
```

## 05b — Query shell results

Queries shell finite element results: in-plane forces (Nxx, Nyy, Mxx, Myy,
Qxx, Qyy) and stresses (Sxx, Syy, von Mises) at the mid, top, and bottom
through-thickness layers.

```{literalinclude} ../examples/05b_query_shell_results.py
:language: python
```

## 06 — Full beam example

Complete end-to-end workflow on a simple 4-node beam: pinned and roller
supports, self-weight and live load cases, a ULS combination, calculation,
and visualisation of the My bending moment diagram with a screenshot.

```{literalinclude} ../examples/06_beam_example.py
:language: python
```

## 07 — Support types

Advanced support definitions covering all available types: rigid (pinned,
fixed, roller), elastic translational and rotational springs, one-directional
(compression-only or tension-only), combined elastic + unilateral, and skewed
supports via alpha/beta/gamma orientation angles.

```{literalinclude} ../examples/07_supports.py
:language: python
```

## 08 — Lattice tower

Parametric triangular lattice tower with ~160 nodes and ~300 members.
Demonstrates the performance benefit of `begin_edit()` for bulk geometry
creation, section database loading, and complex member topologies.

```{literalinclude} ../examples/08_lattice_tower.py
:language: python
```

## 09 — Cladding local coordinate systems

Six cladding panel configurations showing `dir_x` for explicit span direction
control and `flip_z` for surface normal reversal.  Useful for correctly
directing one-way cladding loads.

```{literalinclude} ../examples/09_cladding_local_cs.py
:language: python
```

## 10 — Custom sections

Creates non-standard cross-sections programmatically: circular hollow sections
(CHS / tubes), solid rectangular sections, and rectangular hollow sections
(RHS).  Also demonstrates assigning different sections to individual bars after
creation.

```{literalinclude} ../examples/10_sections.py
:language: python
```

## 11 — Timber roof truss

Full parametric timber roof truss: geometry generation, material and section
assignment, load cases, combinations, calculation, and result extraction.

```{literalinclude} ../examples/11_timber_roof_truss.py
:language: python
```
