import sys
import os

# Ensure the project root is in the python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from gui.app import ParquetViewerApp

def main():
    # Set taskbar icon correctly on Windows by declaring a unique AppUserModelID
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("antigravity.parquetviewer.1.0")
        except Exception:
            pass

    # Set up High-DPI scaling attributes for modern high-resolution displays
    # (Note: PySide6/Qt6 handles many scaling features automatically, but we ensure standard behavior)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    
    # Set the style to "Fusion" as a clean base for our custom premium styling sheet
    app.setStyle("Fusion")
    
    viewer = ParquetViewerApp()
    viewer.show()
    
    # If a file path is passed as a command-line argument, load it immediately!
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path) and file_path.lower().endswith(('.parquet', '.pq')):
            viewer.load_parquet_file(file_path)
            
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
