"""
Test script to check Qt installation
"""
import sys

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("\nTrying to import Qt backends...\n")

# Test PyQt5
try:
    import PyQt5.QtWidgets
    print("✓ PyQt5 is installed and working!")
    print("  Version:", PyQt5.QtCore.QT_VERSION_STR)
except ImportError as e:
    print("✗ PyQt5 not available:", str(e))

# Test PySide2
try:
    import PySide2.QtWidgets
    print("✓ PySide2 is installed and working!")
    print("  Version:", PySide2.QtCore.__version__)
except ImportError as e:
    print("✗ PySide2 not available:", str(e))

# Test PySide6
try:
    import PySide6.QtWidgets
    print("✓ PySide6 is installed and working!")
    print("  Version:", PySide6.__version__)
except ImportError as e:
    print("✗ PySide6 not available:", str(e))

print("\n" + "="*50)
print("RECOMMENDATION:")
print("="*50)
print("Open Anaconda Prompt and run:")
print("  conda activate OccView")
print("  conda install -c conda-forge pyqt")
