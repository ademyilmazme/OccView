"""
Main application window with UI layout and user interactions
"""
from .qt_compat import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QStatusBar, QMenuBar, QMenu,
    QToolBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QLabel, Qt
)
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

from .viewer import Viewer
from .primitives import make_box, make_sphere, make_cylinder, translate_shape


class MainWindow(QMainWindow):
    """
    Main application window

    Provides a model tree, 3D viewer, menu bar, toolbar, and status bar
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OccView")
        self.setGeometry(100, 100, 1400, 900)

        # Shape positioning counter (each shape offset by 120mm in X)
        self.shape_counter = 0

        # Mapping: tree item -> AIS_Shape object
        self._item_to_ais = {}

        # Display mode state
        self._is_wireframe = False
        self._trihedron_visible = True

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

        # Setup UI components
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()

    def _setup_menu_bar(self):
        """Create the menu bar with File, View, Tools, Help menus"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        self._action_open = QAction("Open STEP/IGES...", self)
        self._action_open.triggered.connect(self._on_open_file)
        file_menu.addAction(self._action_open)

        self._action_export = QAction("Export STEP...", self)
        self._action_export.triggered.connect(self._on_export_file)
        file_menu.addAction(self._action_export)

        file_menu.addSeparator()

        self._action_exit = QAction("Exit", self)
        self._action_exit.triggered.connect(self.close)
        file_menu.addAction(self._action_exit)

        # View menu
        view_menu = menubar.addMenu("View")

        self._action_fit_all = QAction("Fit All", self)
        self._action_fit_all.triggered.connect(self._on_fit_all)
        view_menu.addAction(self._action_fit_all)

        view_menu.addSeparator()

        self._action_toggle_wireframe = QAction("Toggle Wireframe/Shaded", self)
        self._action_toggle_wireframe.triggered.connect(self._on_toggle_wireframe)
        view_menu.addAction(self._action_toggle_wireframe)

        self._action_toggle_trihedron = QAction("Toggle Trihedron", self)
        self._action_toggle_trihedron.triggered.connect(self._on_toggle_trihedron)
        view_menu.addAction(self._action_toggle_trihedron)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        self._action_add_box = QAction("Add Box", self)
        self._action_add_box.triggered.connect(self._on_add_box)
        tools_menu.addAction(self._action_add_box)

        self._action_add_sphere = QAction("Add Sphere", self)
        self._action_add_sphere.triggered.connect(self._on_add_sphere)
        tools_menu.addAction(self._action_add_sphere)

        self._action_add_cylinder = QAction("Add Cylinder", self)
        self._action_add_cylinder.triggered.connect(self._on_add_cylinder)
        tools_menu.addAction(self._action_add_cylinder)

        tools_menu.addSeparator()

        self._action_clear = QAction("Clear Scene", self)
        self._action_clear.triggered.connect(self._on_clear)
        tools_menu.addAction(self._action_clear)

        # Help menu
        help_menu = menubar.addMenu("Help")

        self._action_about = QAction("About", self)
        self._action_about.triggered.connect(self._on_about)
        help_menu.addAction(self._action_about)

    def _setup_toolbar(self):
        """Create the toolbar with common actions"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self._action_open)
        toolbar.addSeparator()
        toolbar.addAction(self._action_fit_all)
        toolbar.addSeparator()
        toolbar.addAction(self._action_add_box)
        toolbar.addAction(self._action_add_sphere)
        toolbar.addAction(self._action_add_cylinder)
        toolbar.addSeparator()
        toolbar.addAction(self._action_clear)

    def _setup_central_widget(self):
        """Create the central widget with splitter containing tree and viewer"""
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)

        # Create model tree
        self._tree = QTreeWidget()
        self._tree.setHeaderLabel("Model Tree")
        self._tree.setMinimumWidth(180)
        self._tree.setMaximumWidth(300)
        self._tree.itemClicked.connect(self._on_tree_item_clicked)

        # Create 3D viewer
        self.viewer = Viewer()
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewer.setMinimumWidth(400)

        # Add widgets to splitter
        splitter.addWidget(self._tree)
        splitter.addWidget(self.viewer)

        # Set stretch factors: tree doesn't stretch, viewer stretches
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # Set initial sizes
        splitter.setSizes([200, 1200])

        # Set splitter as central widget
        self.setCentralWidget(splitter)

    def _setup_status_bar(self):
        """Create the status bar with messages and mouse hints"""
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)

        # Add permanent mouse hints on the right
        mouse_hints = QLabel("LMB rotate | MMB pan | Wheel zoom")
        self._status_bar.addPermanentWidget(mouse_hints)

        # Show initial message
        self._status_bar.showMessage("Ready")

    def _get_next_color(self):
        """Get the next color from the color palette"""
        color = self.colors[self.shape_counter % len(self.colors)]
        return color

    def _get_translation_offset(self):
        """Get X-axis translation offset for current shape"""
        return self.shape_counter * 120

    def _add_shape_to_tree(self, shape_type, ais_shape):
        """
        Add a shape entry to the model tree

        Args:
            shape_type: String name of the shape type (Box, Sphere, Cylinder)
            ais_shape: The AIS_Shape object to associate with this tree item
        """
        item_name = f"{shape_type} {self.shape_counter + 1}"
        item = QTreeWidgetItem([item_name])
        self._tree.addTopLevelItem(item)
        self._item_to_ais[id(item)] = ais_shape

    def _on_tree_item_clicked(self, item, column):
        """Handle tree item click to select shape in viewer"""
        item_id = id(item)
        if item_id in self._item_to_ais:
            ais_shape = self._item_to_ais[item_id]
            self.viewer.select_ais_shape(ais_shape)
            self._status_bar.showMessage(f"Selected: {item.text(0)}")

    def _on_add_box(self):
        """Add a box primitive to the scene"""
        box = make_box(dx=80, dy=50, dz=30)
        x_offset = self._get_translation_offset()
        box_translated = translate_shape(box, x=x_offset, y=0, z=0)
        color = self._get_next_color()
        ais_shape = self.viewer.display_shape(box_translated, color=color)
        self._add_shape_to_tree("Box", ais_shape)
        self._status_bar.showMessage(f"Added Box #{self.shape_counter + 1}")
        self.shape_counter += 1

    def _on_add_sphere(self):
        """Add a sphere primitive to the scene"""
        sphere = make_sphere(r=25)
        x_offset = self._get_translation_offset()
        sphere_translated = translate_shape(sphere, x=x_offset, y=0, z=0)
        color = self._get_next_color()
        ais_shape = self.viewer.display_shape(sphere_translated, color=color)
        self._add_shape_to_tree("Sphere", ais_shape)
        self._status_bar.showMessage(f"Added Sphere #{self.shape_counter + 1}")
        self.shape_counter += 1

    def _on_add_cylinder(self):
        """Add a cylinder primitive to the scene"""
        cylinder = make_cylinder(r=15, h=60)
        x_offset = self._get_translation_offset()
        cylinder_translated = translate_shape(cylinder, x=x_offset, y=0, z=0)
        color = self._get_next_color()
        ais_shape = self.viewer.display_shape(cylinder_translated, color=color)
        self._add_shape_to_tree("Cylinder", ais_shape)
        self._status_bar.showMessage(f"Added Cylinder #{self.shape_counter + 1}")
        self.shape_counter += 1

    def _on_clear(self):
        """Clear all shapes from the scene and tree"""
        self.viewer.clear()
        self._tree.clear()
        self._item_to_ais.clear()
        self.shape_counter = 0
        self._status_bar.showMessage("Cleared scene")

    def _on_fit_all(self):
        """Fit all shapes in the viewer"""
        self.viewer.fit_all()
        self._status_bar.showMessage("Fit All")

    def _on_open_file(self):
        """Open a STEP or IGES file (stub)"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open STEP/IGES File",
            "",
            "CAD Files (*.step *.stp *.iges *.igs);;All Files (*)"
        )
        if file_path:
            self._status_bar.showMessage(f"Open file: {file_path} (not implemented)")

    def _on_export_file(self):
        """Export to STEP file (stub)"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export STEP File",
            "",
            "STEP Files (*.step *.stp);;All Files (*)"
        )
        if file_path:
            self._status_bar.showMessage(f"Export to: {file_path} (not implemented)")

    def _on_toggle_wireframe(self):
        """Toggle between wireframe and shaded display modes"""
        if self._is_wireframe:
            self.viewer.set_display_mode_shaded()
            self._status_bar.showMessage("Display mode: Shaded")
        else:
            self.viewer.set_display_mode_wireframe()
            self._status_bar.showMessage("Display mode: Wireframe")
        self._is_wireframe = not self._is_wireframe

    def _on_toggle_trihedron(self):
        """Toggle the trihedron (axis) visibility"""
        self._trihedron_visible = not self._trihedron_visible
        self.viewer.toggle_trihedron(self._trihedron_visible)
        state = "visible" if self._trihedron_visible else "hidden"
        self._status_bar.showMessage(f"Trihedron: {state}")

    def _on_about(self):
        """Show the About dialog"""
        QMessageBox.about(
            self,
            "About OccView",
            "OccView v1.0.0\n\n"
            "A 3D CAD Viewer built with PythonOCC and Qt.\n\n"
            "License: GNU GPLv3"
        )
