import os
import sys

# Add src/ to path so autodoc can import the package without installing it
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -------------------------------------------------------
project = "pyrobotstructural"
copyright = "2024, m-wolin"
author = "m-wolin"
release = "0.1.0"

# -- General configuration -----------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Mock Windows-only imports so the docs build succeeds on Linux (ReadTheDocs).
# `clr` is provided by pythonnet and is only usable on Windows with Robot installed.
autodoc_mock_imports = ["clr", "win32clipboard", "win32con", "win32api", "win32gui"]

# -- Napoleon (NumPy-style docstrings) ----------------------------------------
napoleon_numpy_docstring = True
napoleon_google_docstring = False

# -- Autodoc ------------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"

# -- HTML output --------------------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
html_title = "pyrobotstructural"
