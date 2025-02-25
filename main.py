import pymel.core as pm
import random

# Preset colors
preset_colors = [
    (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 0.0, 1.0),
    (0.0, 1.0, 1.0), (0.5, 0.0, 0.0), (0.0, 0.5, 0.0), (0.0, 0.0, 0.5), (0.5, 0.5, 0.0),
    (0.5, 0.0, 0.5), (0.0, 0.5, 0.5), (0.75, 0.25, 0.25), (0.25, 0.75, 0.25), (0.25, 0.25, 0.75),
    (0.75, 0.75, 0.25), (0.75, 0.25, 0.75), (0.25, 0.75, 0.75), (0.9, 0.4, 0.1), (0.4, 0.9, 0.1)
]

# List to store colors flooded
used_colors = []
selected_color = None

# Function to generate random (and unique) color to faces selected.
def generate_unique_color():
    global used_colors
    available_colors = [color for color in preset_colors if color not in used_colors]

    if not available_colors:
        pm.warning("All preset colors have been used. Using random color.")
        return random.choice(preset_colors)

    color = random.choice(available_colors)
    used_colors.append(color)
    return color

# Paint faces selected with the selected color
def paint_vertices(*args):
    global selected_color
    selection = pm.ls(selection=True, flatten=True)

    if not selection:
        pm.warning("No faces selected.")
        return

    color = selected_color if selected_color else generate_unique_color()

    for face in selection:
        verts = pm.polyListComponentConversion(face, toVertex=True)
        pm.polyColorPerVertex(verts, rgb=color, colorDisplayOption=True)
        pm.polyColorPerVertex(verts, colorRGB=color, cdo=True)

    pm.select(selection)

# Clear vertex paint colors from selected faces
def clear_vertices(*args):
    selection = pm.ls(selection=True, flatten=True)

    if not selection:
        pm.warning("No faces selected.")
        return

    for face in selection:
        verts = pm.polyListComponentConversion(face, toVertex=True)
        pm.polyColorPerVertex(verts, rgb=(1, 1, 1), colorDisplayOption=False)

    pm.select(selection)

# Set selected color in the preset colors.
def select_color(color, *args):
    global selected_color
    selected_color = color
    pm.inViewMessage(amg=f"<hl>Selected color:</hl> {color}", pos='topCenter', fade=True)

# Create UI
def create_ui():
    window_name = "Easy.VertexPaint"

    if pm.window(window_name, exists=True):
        pm.deleteUI(window_name, window=True)

    with pm.window(window_name, title="Easy.VertexPaint", widthHeight=(250, 300)):
        with pm.columnLayout(adjustableColumn=True, rowSpacing=10):
            pm.text(label="Vertex Paint with a click.", align='center', height=30)
            pm.text(label="Select a color:", align='center')
            with pm.gridLayout(numberOfColumns=5, cellWidthHeight=(40, 40)):
                for color in preset_colors:
                    pm.button(backgroundColor=color, command=lambda x, c=color: select_color(c))

            pm.separator(height=10)
            pm.button(label="Paint it!", height=40, command=paint_vertices)
            pm.button(label="Clear it!", height=40, command=clear_vertices)

    pm.showWindow(window_name)

# Execute main function
def main():
    create_ui()

main()
