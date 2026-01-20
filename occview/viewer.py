"""
PythonOCC Qt Viewer Wrapper
Provides a clean interface to the PythonOCC 3D viewer
"""
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID

from .qt_compat import QSizePolicy


# Selection mode mapping: mode name -> AIS_Shape selection mode integer
# AIS_Shape selection modes:
#   0 = whole shape (default object selection)
#   1 = vertex
#   2 = edge
#   4 = face
#   6 = solid
SELECTION_MODES = {
    "vertex": 1,
    "edge": 2,
    "face": 4,
    "solid": 0,  # 0 selects the whole AIS object
}


class Viewer(qtViewer3d):
    """
    Wrapper around PythonOCC Qt viewer

    Provides simplified interface for displaying and managing shapes
    """

    def __init__(self):
        super().__init__()

        # Initialize the graphics driver
        self.InitDriver()

        # Get the display handle
        self._display = self._display

        # Track displayed AIS objects for clearing
        self._ais_shapes = []

        # Default color for shapes
        self._default_color = Quantity_Color(0.7, 0.7, 0.7, Quantity_TOC_RGB)

        # Current selection mode
        self._current_selection_mode = "face"

        # Set size policy to expanding so it fills available space
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def display_shape(self, shape, color=None):
        """
        Display a TopoDS_Shape in the viewer

        Args:
            shape: TopoDS_Shape to display
            color: Quantity_Color for the shape (uses default if None)

        Returns:
            AIS_Shape: The created AIS interactive object
        """
        if color is None:
            color = self._default_color

        # Create AIS interactive shape
        ais_shape = AIS_Shape(shape)

        # Get the AIS context and display
        context = self._display.Context
        context.Display(ais_shape, True)
        context.SetColor(ais_shape, color, True)

        # Track for later removal
        self._ais_shapes.append(ais_shape)

        # Apply current selection mode to the new shape
        self._apply_selection_mode_to_shape(ais_shape)

        # Update the viewer
        self._display.Repaint()

        return ais_shape

    def clear(self):
        """Remove all shapes from the viewer"""
        context = self._display.Context

        # Remove all tracked AIS shapes
        for ais_shape in self._ais_shapes:
            context.Remove(ais_shape, True)

        # Clear the list
        self._ais_shapes.clear()

        # Update the viewer
        self._display.Repaint()

    def fit_all(self):
        """Adjust camera to fit all visible shapes"""
        self._display.FitAll()

    def select_ais_shape(self, ais_shape):
        """
        Select and highlight an AIS shape in the viewer (for tree selection)

        Args:
            ais_shape: AIS_Shape to select
        """
        context = self._display.Context
        # Clear previous selection
        context.ClearSelected(False)
        # Add the shape to selection
        context.AddOrRemoveSelected(ais_shape, True)
        self._display.Repaint()

    def clear_selection(self):
        """Clear all selections in the viewer"""
        context = self._display.Context
        context.ClearSelected(True)
        self._display.Repaint()

    def set_display_mode_shaded(self):
        """Set display mode to shaded"""
        self._display.SetModeShaded()

    def set_display_mode_wireframe(self):
        """Set display mode to wireframe"""
        self._display.SetModeWireFrame()

    def toggle_trihedron(self, visible):
        """Toggle the trihedron (axis) visibility"""
        if visible:
            self._display.display_trihedron()
        else:
            self._display.hide_trihedron()

    def get_context(self):
        """Get the AIS interactive context"""
        return self._display.Context

    def set_selection_mode(self, mode):
        """
        Set the selection mode for all displayed shapes

        Args:
            mode: One of "vertex", "edge", "face", "solid"
        """
        if mode not in SELECTION_MODES:
            raise ValueError(f"Invalid selection mode: {mode}. "
                           f"Must be one of {list(SELECTION_MODES.keys())}")

        self._current_selection_mode = mode
        context = self._display.Context

        # Clear current selection when changing mode
        context.ClearSelected(False)

        # Deactivate all selection modes for all shapes first
        for ais_shape in self._ais_shapes:
            # Deactivate all possible modes
            for m in [0, 1, 2, 4, 6]:
                context.Deactivate(ais_shape, m)

        # Activate the new selection mode for all shapes
        new_mode = SELECTION_MODES[mode]
        for ais_shape in self._ais_shapes:
            context.Activate(ais_shape, new_mode)

        self._display.Repaint()

    def _apply_selection_mode_to_shape(self, ais_shape):
        """
        Apply the current selection mode to a newly added shape

        Args:
            ais_shape: The AIS_Shape to configure
        """
        context = self._display.Context
        mode = SELECTION_MODES[self._current_selection_mode]

        # Deactivate default mode (0) if we're using sub-shape selection
        if mode != 0:
            context.Deactivate(ais_shape, 0)

        # Activate the current selection mode
        context.Activate(ais_shape, mode)

    def get_current_selection_mode(self):
        """Get the current selection mode name"""
        return self._current_selection_mode

    def get_selection_summary(self):
        """
        Get a summary of currently selected entities

        Returns:
            str: Description of selected items (e.g., "Faces selected: 2")
        """
        context = self._display.Context

        # Count selected items by type
        vertex_count = 0
        edge_count = 0
        face_count = 0
        solid_count = 0
        shape_count = 0

        # Iterate through selected items
        context.InitSelected()
        while context.MoreSelected():
            if context.HasSelectedShape():
                selected_shape = context.SelectedShape()
                shape_type = selected_shape.ShapeType()

                if shape_type == TopAbs_VERTEX:
                    vertex_count += 1
                elif shape_type == TopAbs_EDGE:
                    edge_count += 1
                elif shape_type == TopAbs_FACE:
                    face_count += 1
                elif shape_type == TopAbs_SOLID:
                    solid_count += 1
                else:
                    shape_count += 1
            else:
                # Whole AIS object selected (not sub-shape)
                shape_count += 1

            context.NextSelected()

        # Build summary string
        parts = []
        if vertex_count > 0:
            parts.append(f"Vertices: {vertex_count}")
        if edge_count > 0:
            parts.append(f"Edges: {edge_count}")
        if face_count > 0:
            parts.append(f"Faces: {face_count}")
        if solid_count > 0:
            parts.append(f"Solids: {solid_count}")
        if shape_count > 0:
            parts.append(f"Objects: {shape_count}")

        if not parts:
            return "No selection"

        return "\n".join(parts)
