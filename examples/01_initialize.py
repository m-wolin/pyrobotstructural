"""
This example shows how to initialize connection with Autodesk Robot. To verify connection, one node is added.
NOTE: You need to open a blank Robot model before execution of this script.
"""

import pyrobotstructural  # 'import pyrobotstructural as pyrbt' or similar abbreviation can be optionally used

# Path can differ, update it according to your needs. It usually requires version number update.
dll_path = r"C:\Program Files\Autodesk\Robot Structural Analysis Professional 2026\Exe\Interop.RobotOM.dll"


pyrobotstructural.initialize(dll_path)

app = pyrobotstructural.RobotApp()

# --- MVerify ---
# To verify if connection works, lets add a node to the model.
app.model.geometry.add_node(1, 0, 0, 0)
