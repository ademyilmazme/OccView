"""
Check Python environment and PyQt5 installation
"""
import sys
import subprocess

print("="*60)
print("PYTHON ENVIRONMENT CHECK")
print("="*60)
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"\nPython path:")
for path in sys.path:
    print(f"  {path}")

print("\n" + "="*60)
print("CHECKING PyQt5...")
print("="*60)

try:
    import PyQt5
    print("✓ PyQt5 module found!")
    print(f"  Location: {PyQt5.__file__}")

    try:
        from PyQt5 import QtCore
        print(f"  Qt version: {QtCore.QT_VERSION_STR}")
        print(f"  PyQt version: {QtCore.PYQT_VERSION_STR}")
    except Exception as e:
        print(f"  Warning: {e}")

    try:
        from PyQt5.QtWidgets import QApplication
        print("✓ PyQt5.QtWidgets imports successfully!")
    except Exception as e:
        print(f"✗ Error importing QtWidgets: {e}")

except ImportError as e:
    print(f"✗ PyQt5 not found: {e}")

print("\n" + "="*60)
print("CONDA ENVIRONMENT INFO")
print("="*60)

try:
    result = subprocess.run(['conda', 'info', '--envs'],
                          capture_output=True, text=True, timeout=5)
    print(result.stdout)
except Exception as e:
    print(f"Could not run conda command: {e}")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print("If PyQt5 is installed in a conda environment,")
print("make sure you're running Python from that environment:")
print("  conda activate OccView")
print("  python check_env.py")
