"""
PythonOCC Qt Viewer Wrapper
Provides a clean interface to the PythonOCC 3D viewer
"""
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

from .qt_compat import QSizePolicy


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
        Select and highlight an AIS shape in the viewer

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
