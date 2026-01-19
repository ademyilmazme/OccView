"""
Main application window with UI layout and user interactions
"""
from .qt_compat import (QMainWindow, QWidget, QVBoxLayout,
                        QHBoxLayout, QPushButton, Qt)
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

from .viewer import Viewer
from .primitives import make_box, make_sphere, make_cylinder, translate_shape


class MainWindow(QMainWindow):
    """
    Main application window

    Provides a sidebar with primitive creation buttons and a 3D viewer
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OccView")
        self.setGeometry(100, 100, 1400, 900)

        # Shape positioning counter (each shape offset by 120mm in X)
        self.shape_counter = 0

        # Color palette for cycling through shapes
        self.colors = [
            Quantity_Color(0.9, 0.1, 0.1, Quantity_TOC_RGB),  # Red
            Quantity_Color(0.1, 0.8, 0.1, Quantity_TOC_RGB),  # Green
            Quantity_Color(0.1, 0.3, 0.9, Quantity_TOC_RGB),  # Blue
            Quantity_Color(0.9, 0.8, 0.0, Quantity_TOC_RGB),  # Yellow
            Quantity_Color(0.8, 0.1, 0.8, Quantity_TOC_RGB),  # Magenta
            Quantity_Color(0.0, 0.8, 0.8, Quantity_TOC_RGB),  # Cyan
            Quantity_Color(0.9, 0.5, 0.1, Quantity_TOC_RGB),  # Orange
        ]

        # Setup UI and viewer
        self._setup_ui()

    def _setup_ui(self):
        """Create and layout all UI components"""
        # Central widget with horizontal layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Left sidebar
        sidebar = self._create_sidebar()

        # 3D Viewer
        self.viewer = Viewer()

        # Add to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.viewer, stretch=1)

    def _create_sidebar(self):
        """Create the left sidebar with control buttons"""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setMaximumWidth(200)
        sidebar_widget.setMinimumWidth(150)

        # Primitive creation buttons
        btn_box = QPushButton("Add Box")
        btn_sphere = QPushButton("Add Sphere")
        btn_cylinder = QPushButton("Add Cylinder")

        # Scene control buttons
        btn_clear = QPushButton("Clear")
        btn_fit = QPushButton("Fit All")

        # Connect signals
        btn_box.clicked.connect(self._on_add_box)
        btn_sphere.clicked.connect(self._on_add_sphere)
        btn_cylinder.clicked.connect(self._on_add_cylinder)
        btn_clear.clicked.connect(self._on_clear)
        btn_fit.clicked.connect(self._on_fit_all)

        # Add to layout
        sidebar_layout.addWidget(btn_box)
        sidebar_layout.addWidget(btn_sphere)
        sidebar_layout.addWidget(btn_cylinder)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(btn_clear)
        sidebar_layout.addWidget(btn_fit)
        sidebar_layout.addStretch()

        return sidebar_widget

    def _get_next_color(self):
        """Get the next color from the color palette"""
        color = self.colors[self.shape_counter % len(self.colors)]
        return color

    def _get_translation_offset(self):
        """Get X-axis translation offset for current shape"""
        return self.shape_counter * 120

    def _on_add_box(self):
        """Add a box primitive to the scene"""
        # Create box
        box = make_box(dx=80, dy=50, dz=30)

        # Translate to avoid overlap
        x_offset = self._get_translation_offset()
        box_translated = translate_shape(box, x=x_offset, y=0, z=0)

        # Display with color
        color = self._get_next_color()
        self.viewer.display_shape(box_translated, color=color)

        # Increment counter
        self.shape_counter += 1

    def _on_add_sphere(self):
        """Add a sphere primitive to the scene"""
        # Create sphere
        sphere = make_sphere(r=25)

        # Translate to avoid overlap
        x_offset = self._get_translation_offset()
        sphere_translated = translate_shape(sphere, x=x_offset, y=0, z=0)

        # Display with color
        color = self._get_next_color()
        self.viewer.display_shape(sphere_translated, color=color)

        # Increment counter
        self.shape_counter += 1

    def _on_add_cylinder(self):
        """Add a cylinder primitive to the scene"""
        # Create cylinder
        cylinder = make_cylinder(r=15, h=60)

        # Translate to avoid overlap
        x_offset = self._get_translation_offset()
        cylinder_translated = translate_shape(cylinder, x=x_offset, y=0, z=0)

        # Display with color
        color = self._get_next_color()
        self.viewer.display_shape(cylinder_translated, color=color)

        # Increment counter
        self.shape_counter += 1

    def _on_clear(self):
        """Clear all shapes from the scene"""
        self.viewer.clear()
        self.shape_counter = 0

    def _on_fit_all(self):
        """Fit all shapes in the viewer"""
        self.viewer.fit_all()
