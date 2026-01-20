"""
Qt compatibility layer - auto-detects and loads Qt backend for pythonocc
"""

QT_BACKEND = None

# Try to import Qt backends in order of preference
# PyQt5 first (most common with conda pythonocc)
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QSplitter, QTreeWidget, QTreeWidgetItem, QStatusBar,
        QMenuBar, QMenu, QToolBar, QAction, QFileDialog, QMessageBox,
        QDockWidget, QSizePolicy, QLabel
    )
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QIcon
    QT_BACKEND = "pyqt5"
except ImportError:
    try:
        from PySide2.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QSplitter, QTreeWidget, QTreeWidgetItem, QStatusBar,
            QMenuBar, QMenu, QToolBar, QAction, QFileDialog, QMessageBox,
            QDockWidget, QSizePolicy, QLabel
        )
        from PySide2.QtCore import Qt
        from PySide2.QtGui import QIcon
        QT_BACKEND = "pyside2"
    except ImportError:
        try:
            from PySide6.QtWidgets import (
                QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                QPushButton, QSplitter, QTreeWidget, QTreeWidgetItem, QStatusBar,
                QMenuBar, QMenu, QToolBar, QFileDialog, QMessageBox,
                QDockWidget, QSizePolicy, QLabel
            )
            from PySide6.QtGui import QAction, QIcon
            from PySide6.QtCore import Qt
            QT_BACKEND = "pyside6"
        except ImportError:
            raise ImportError(
                "No Qt backend found.\n"
                "In your conda environment, run:\n"
                "  conda install pyqt\n"
                "or\n"
                "  conda install pyside2"
            )

# Now load the backend for pythonocc
from OCC.Display.backend import load_backend
load_backend(QT_BACKEND)

__all__ = [
    'QApplication', 'QMainWindow', 'QWidget', 'QVBoxLayout', 'QHBoxLayout',
    'QPushButton', 'QSplitter', 'QTreeWidget', 'QTreeWidgetItem', 'QStatusBar',
    'QMenuBar', 'QMenu', 'QToolBar', 'QAction', 'QFileDialog', 'QMessageBox',
    'QDockWidget', 'QSizePolicy', 'QLabel', 'Qt', 'QIcon', 'QT_BACKEND'
]
