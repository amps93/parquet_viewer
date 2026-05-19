class DarkTheme:
    BG_MAIN = "#121215"
    BG_CARD = "#1a1a22"
    BG_INPUT = "#22222e"
    BORDER_COLOR = "#2e2e3f"
    TEXT_PRIMARY = "#f3f3f6"
    TEXT_SECONDARY = "#9da2b0"
    
    ACCENT_COLOR = "#00f0ff"       # Neon Cyan
    ACCENT_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0077b6, stop:1 #00f0ff)"
    ACCENT_HOVER = "#33f3ff"
    
    SUCCESS_COLOR = "#00f5d4"      # Turquoise/Green
    DANGER_COLOR = "#ff2a6d"       # Neon Pink/Red

class LightTheme:
    BG_MAIN = "#f5f6fa"
    BG_CARD = "#ffffff"
    BG_INPUT = "#eef2f7"
    BORDER_COLOR = "#dcdde1"
    TEXT_PRIMARY = "#2f3640"
    TEXT_SECONDARY = "#718093"
    
    ACCENT_COLOR = "#0080ff"       # Vibrant Blue
    ACCENT_GRADIENT = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0066cc, stop:1 #0080ff)"
    ACCENT_HOVER = "#3399ff"
    
    SUCCESS_COLOR = "#2ecc71"      # Clean Green
    DANGER_COLOR = "#e74c3c"       # Clean Red

class Theme:
    @staticmethod
    def get_style(is_dark: bool = True) -> str:
        t = DarkTheme if is_dark else LightTheme
        import sys
        import os
        
        # Determine the base directory for resources safely (handles PyInstaller ZIP packaging)
        if getattr(sys, 'frozen', False):
            meipass = getattr(sys, '_MEIPASS', '')
            if meipass:
                candidate1 = os.path.join(meipass, "gui")
                candidate2 = os.path.join(meipass, "_internal", "gui")
                if os.path.isdir(candidate1):
                    base_dir = candidate1
                elif os.path.isdir(candidate2):
                    base_dir = candidate2
                else:
                    base_dir = meipass
            else:
                exe_dir = os.path.dirname(sys.executable)
                candidate1 = os.path.join(exe_dir, "_internal", "gui")
                candidate2 = os.path.join(exe_dir, "gui")
                if os.path.isdir(candidate1):
                    base_dir = candidate1
                else:
                    base_dir = candidate2
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        base_dir = base_dir.replace('\\', '/')
        
        return f"""
        /* Main Window and Dialogs */
        QMainWindow, QDialog {{
            background-color: {t.BG_MAIN};
            color: {t.TEXT_PRIMARY};
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            font-size: 13px;
        }}
        
        /* Frame & Cards */
        QFrame#cardFrame, QFrame#sidebarFrame {{
            background-color: {t.BG_CARD};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 8px;
        }}
        
        QSplitter::handle {{
            background-color: {t.BORDER_COLOR};
        }}
        
        QSplitter::handle:horizontal {{
            width: 4px;
        }}
        
        QSplitter::handle:vertical {{
            height: 4px;
        }}

        /* Labels */
        QLabel {{
            color: {t.TEXT_PRIMARY};
        }}
        
        QLabel#titleLabel {{
            font-size: 20px;
            font-weight: bold;
            color: {t.TEXT_PRIMARY};
            background: transparent;
        }}

        QLabel#subtitleLabel {{
            font-size: 12px;
            color: {t.TEXT_SECONDARY};
            background: transparent;
        }}

        QLabel#statusLabel {{
            font-size: 11px;
            color: {t.TEXT_SECONDARY};
        }}
        
        QLabel#metaFileName {{
            font-weight: bold;
            color: {t.ACCENT_COLOR};
        }}
        
        QLabel#paginationInfo {{
            color: {t.TEXT_SECONDARY};
            font-weight: 500;
        }}
        
        QLabel#statusFooter {{
            color: {t.TEXT_SECONDARY};
            font-size: 11px;
            padding: 2px;
        }}
        
        /* Tab Widget & Bar */
        QTabWidget::pane {{
            border: 1px solid {t.BORDER_COLOR};
            background: {t.BG_CARD};
            border-radius: 8px;
            top: -1px;
        }}
        
        QTabBar::tab {{
            background: {t.BG_MAIN};
            color: {t.TEXT_SECONDARY};
            border: 1px solid {t.BORDER_COLOR};
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            font-weight: bold;
        }}
        
        QTabBar::tab:hover {{
            background: {t.BG_CARD};
            color: {t.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:selected {{
            background: {t.BG_CARD};
            color: {t.ACCENT_COLOR};
            border-bottom: 2px solid {t.ACCENT_COLOR};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {t.BG_INPUT};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 12px;
        }}
        
        QPushButton:hover {{
            background-color: {t.BG_MAIN if is_dark else "#e4e7eb"};
            border-color: {t.ACCENT_COLOR};
        }}
        
        QPushButton:pressed {{
            background-color: {t.BORDER_COLOR};
        }}
        
        QPushButton:disabled {{
            background-color: {"#1a1a20" if is_dark else "#eaeaea"};
            color: {"#555565" if is_dark else "#aaaaaa"};
            border-color: {"#22222a" if is_dark else "#dddddd"};
        }}
        
        /* Compact Navigation Buttons */
        QPushButton#navButton {{
            padding: 4px 2px;
            font-size: 11px;
            font-weight: bold;
        }}
        
        /* Primary (Accent) Button */
        QPushButton#primaryButton {{
            background: {t.ACCENT_GRADIENT};
            color: {"#0c0f12" if is_dark else "#ffffff"};
            border: none;
        }}
        
        QPushButton#primaryButton:hover {{
            background: {"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0096c7, stop:1 " + t.ACCENT_HOVER + ")" if is_dark else "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0080ff, stop:1 #3399ff)"};
            border: 1px solid {t.ACCENT_HOVER};
        }}
        
        QPushButton#primaryButton:pressed {{
            background: {"#0077b6" if is_dark else "#0055b3"};
        }}

        /* Danger Button */
        QPushButton#dangerButton {{
            background-color: transparent;
            color: {t.DANGER_COLOR};
            border: 1px solid {t.DANGER_COLOR};
        }}
        
        QPushButton#dangerButton:hover {{
            background-color: {t.DANGER_COLOR};
            color: #ffffff;
        }}
        
        /* Text Inputs */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {t.BG_INPUT};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px;
            selection-background-color: {t.ACCENT_COLOR};
            selection-color: #121215;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {t.ACCENT_COLOR};
        }}
        
        /* Tables */
        QTableView {{
            background-color: {t.BG_CARD};
            alternate-background-color: {"#22222f" if is_dark else "#f9fafb"};
            color: {t.TEXT_PRIMARY};
            gridline-color: {t.BORDER_COLOR};
            border: 0px;
            border-radius: 4px;
            selection-background-color: {"rgba(0, 240, 255, 0.15)" if is_dark else "rgba(0, 128, 255, 0.15)"};
            selection-color: {t.TEXT_PRIMARY};
        }}
        
        QHeaderView::section {{
            background-color: {t.BG_MAIN};
            color: {t.TEXT_SECONDARY};
            padding: 8px;
            border: 0px;
            border-bottom: 2px solid {t.BORDER_COLOR};
            border-right: 1px solid {t.BORDER_COLOR};
            font-weight: bold;
            font-size: 11px;
        }}
        
        QHeaderView::section:hover {{
            background-color: {t.BG_CARD};
            color: {t.TEXT_PRIMARY};
        }}
        
        QTableCornerButton::section {{
            background-color: {t.BG_MAIN};
            border: 0px;
        }}

        /* Combo Boxes */
        QComboBox {{
            background-color: {t.BG_INPUT};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 6px;
            padding: 6px 12px;
            min-width: 100px;
        }}
        
        QComboBox:hover {{
            border-color: {t.ACCENT_COLOR};
        }}
        
        QComboBox:on {{
            border-color: {t.ACCENT_COLOR};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 0px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {t.BG_CARD};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.BORDER_COLOR};
            selection-background-color: {"rgba(0, 240, 255, 0.2)" if is_dark else "rgba(0, 128, 255, 0.2)"};
            selection-color: {t.TEXT_PRIMARY};
        }}
        
        /* ===================== Scrollbars ===================== */

        /* --- Vertical Scrollbar --- */
        QScrollBar:vertical {{
            border: none;
            background: {t.BG_MAIN};
            width: 16px;
            margin: 16px 0px 16px 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {"#3e3e50" if is_dark else "#cbd5e1"};
            min-height: 20px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::sub-line:vertical {{
            border: 1px solid {t.BORDER_COLOR};
            background: {t.BG_INPUT};
            height: 16px;
            subcontrol-position: top;
            subcontrol-origin: margin;
            border-radius: 3px;
        }}
        
        QScrollBar::sub-line:vertical:hover {{
            background: {"#2e2e40" if is_dark else "#dde3ec"};
            border-color: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::add-line:vertical {{
            border: 1px solid {t.BORDER_COLOR};
            background: {t.BG_INPUT};
            height: 16px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            border-radius: 3px;
        }}
        
        QScrollBar::add-line:vertical:hover {{
            background: {"#2e2e40" if is_dark else "#dde3ec"};
            border-color: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::up-arrow:vertical {{
            width: 14px;
            height: 14px;
            image: url("{base_dir}/up_arrow.png");
        }}
        
        QScrollBar::down-arrow:vertical {{
            width: 14px;
            height: 14px;
            image: url("{base_dir}/down_arrow.png");
        }}
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}

        /* --- Horizontal Scrollbar --- */
        QScrollBar:horizontal {{
            border: none;
            background: {t.BG_MAIN};
            height: 16px;
            margin: 0px 16px 0px 16px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {"#3e3e50" if is_dark else "#cbd5e1"};
            min-width: 20px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::sub-line:horizontal {{
            border: 1px solid {t.BORDER_COLOR};
            background: {t.BG_INPUT};
            width: 16px;
            subcontrol-position: left;
            subcontrol-origin: margin;
            border-radius: 3px;
        }}
        
        QScrollBar::sub-line:horizontal:hover {{
            background: {"#2e2e40" if is_dark else "#dde3ec"};
            border-color: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::add-line:horizontal {{
            border: 1px solid {t.BORDER_COLOR};
            background: {t.BG_INPUT};
            width: 16px;
            subcontrol-position: right;
            subcontrol-origin: margin;
            border-radius: 3px;
        }}
        
        QScrollBar::add-line:horizontal:hover {{
            background: {"#2e2e40" if is_dark else "#dde3ec"};
            border-color: {t.ACCENT_COLOR};
        }}
        
        QScrollBar::left-arrow:horizontal {{
            width: 14px;
            height: 14px;
            image: url("{base_dir}/left_arrow.png");
        }}
        
        QScrollBar::right-arrow:horizontal {{
            width: 14px;
            height: 14px;
            image: url("{base_dir}/right_arrow.png");
        }}
        
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
        
        /* Group Boxes */
        QGroupBox {{
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 8px;
            margin-top: 1.5ex;
            font-weight: bold;
            color: {t.ACCENT_COLOR};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
        }}
        
        /* List View / Tree View */
        QListView, QTreeView {{
            background-color: {t.BG_CARD};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 6px;
            padding: 4px;
            selection-background-color: {"rgba(0, 240, 255, 0.15)" if is_dark else "rgba(0, 128, 255, 0.15)"};
            selection-color: {t.TEXT_PRIMARY};
        }}
        
        QListView::item, QTreeView::item {{
            padding: 6px 8px;
            border-radius: 4px;
        }}
        
        QListView::item:hover, QTreeView::item:hover {{
            background-color: {"rgba(255, 255, 255, 0.05)" if is_dark else "rgba(0, 0, 0, 0.03)"};
        }}
        
        QListView::item:selected, QTreeView::item:selected {{
            background-color: {"rgba(0, 240, 255, 0.2)" if is_dark else "rgba(0, 128, 255, 0.2)"};
            color: {t.TEXT_PRIMARY};
            font-weight: bold;
        }}
        
        /* ToolTip */
        QToolTip {{
            background-color: {t.BG_CARD};
            color: {t.TEXT_PRIMARY};
            border: 1px solid {t.ACCENT_COLOR};
            border-radius: 4px;
            padding: 4px;
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background-color: {t.BG_INPUT};
            border: 1px solid {t.BORDER_COLOR};
            border-radius: 4px;
            text-align: center;
            color: {t.TEXT_PRIMARY};
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: {t.ACCENT_COLOR};
            border-radius: 3px;
        }}
        """
