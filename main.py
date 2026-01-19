"""
OccView - PythonOCC Qt Viewer
Entry point for the application
"""
import sys
from occview.qt_compat import QApplication, QT_BACKEND
from occview.app import MainWindow


def main():
    """Application entry point"""
    print(f"Using Qt backend: {QT_BACKEND}")

    app = QApplication(sys.argv)
    try:
        app.setStyle('Fusion')
    except:
        pass  # Fusion style may not be available

    window = MainWindow()
    window.show()

    sys.exit(app.exec() if hasattr(app, 'exec') else app.exec_())


if __name__ == "__main__":
    main()