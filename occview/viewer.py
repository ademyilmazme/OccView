"""
PythonOCC Qt Viewer Wrapper
Provides a clean interface to the PythonOCC 3D viewer
"""
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB


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

    def display_shape(self, shape, color=None):
        """
        Display a TopoDS_Shape in the viewer

        Args:
            shape: TopoDS_Shape to display
            color: Quantity_Color for the shape (uses default if None)
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
