class Theme:
    # Modern dark color palette
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
    
    QSS = f"""
    /* Main Window and Dialogs */
    QMainWindow, QDialog {{
        background-color: {BG_MAIN};
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        font-size: 13px;
    }}
    
    /* Frame & Cards */
    QFrame#cardFrame, QFrame#sidebarFrame {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER_COLOR};
        border-radius: 8px;
    }}
    
    QSplitter::handle {{
        background-color: {BORDER_COLOR};
    }}
    
    QSplitter::handle:horizontal {{
        width: 4px;
    }}
    
    QSplitter::handle:vertical {{
        height: 4px;
    }}

    /* Labels */
    QLabel {{
        color: {TEXT_PRIMARY};
    }}
    
    QLabel#titleLabel {{
        font-size: 20px;
        font-weight: bold;
        color: {TEXT_PRIMARY};
        background: transparent;
    }}

    QLabel#subtitleLabel {{
        font-size: 12px;
        color: {TEXT_SECONDARY};
        background: transparent;
    }}

    QLabel#statusLabel {{
        font-size: 11px;
        color: {TEXT_SECONDARY};
    }}
    
    /* Tab Widget & Bar */
    QTabWidget::pane {{
        border: 1px solid {BORDER_COLOR};
        background: {BG_CARD};
        border-radius: 8px;
        top: -1px;
    }}
    
    QTabBar::tab {{
        background: {BG_MAIN};
        color: {TEXT_SECONDARY};
        border: 1px solid {BORDER_COLOR};
        border-bottom-color: transparent;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 8px 16px;
        margin-right: 4px;
        font-weight: bold;
    }}
    
    QTabBar::tab:hover {{
        background: {BG_CARD};
        color: {TEXT_PRIMARY};
    }}
    
    QTabBar::tab:selected {{
        background: {BG_CARD};
        color: {ACCENT_COLOR};
        border-bottom: 2px solid {ACCENT_COLOR};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 12px;
    }}
    
    QPushButton:hover {{
        background-color: #2c2c3d;
        border-color: {ACCENT_COLOR};
    }}
    
    QPushButton:pressed {{
        background-color: {BORDER_COLOR};
    }}
    
    QPushButton:disabled {{
        background-color: #1a1a20;
        color: #555565;
        border-color: #22222a;
    }}
    
    /* Primary (Accent) Button */
    QPushButton#primaryButton {{
        background: {ACCENT_GRADIENT};
        color: #0c0f12;
        border: none;
    }}
    
    QPushButton#primaryButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0096c7, stop:1 {ACCENT_HOVER});
        /* Subtle glow */
        border: 1px solid {ACCENT_HOVER};
    }}
    
    QPushButton#primaryButton:pressed {{
        background: #0077b6;
    }}

    /* Danger Button */
    QPushButton#dangerButton {{
        background-color: transparent;
        color: {DANGER_COLOR};
        border: 1px solid {DANGER_COLOR};
    }}
    
    QPushButton#dangerButton:hover {{
        background-color: {DANGER_COLOR};
        color: #ffffff;
    }}
    
    /* Text Inputs */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 8px;
        selection-background-color: {ACCENT_COLOR};
        selection-color: #121215;
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 1px solid {ACCENT_COLOR};
    }}
    
    /* Tables */
    QTableView {{
        background-color: {BG_CARD};
        alternate-background-color: #22222f;
        color: {TEXT_PRIMARY};
        gridline-color: {BORDER_COLOR};
        border: 0px;
        border-radius: 4px;
        selection-background-color: rgba(0, 240, 255, 0.15);
        selection-color: {TEXT_PRIMARY};
    }}
    
    QHeaderView::section {{
        background-color: {BG_MAIN};
        color: {TEXT_SECONDARY};
        padding: 8px;
        border: 0px;
        border-bottom: 2px solid {BORDER_COLOR};
        border-right: 1px solid {BORDER_COLOR};
        font-weight: bold;
        font-size: 11px;
    }}
    
    QHeaderView::section:hover {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
    }}
    
    QTableCornerButton::section {{
        background-color: {BG_MAIN};
        border: 0px;
    }}

    /* Combo Boxes */
    QComboBox {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 100px;
    }}
    
    QComboBox:hover {{
        border-color: {ACCENT_COLOR};
    }}
    
    QComboBox:on {{
        border-color: {ACCENT_COLOR};
    }}
    
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 0px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        selection-background-color: rgba(0, 240, 255, 0.2);
        selection-color: {TEXT_PRIMARY};
    }}
    
    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: {BG_MAIN};
        width: 10px;
        margin: 0px;
    }}
    
    QScrollBar::handle:vertical {{
        background: #3e3e50;
        min-height: 20px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {ACCENT_COLOR};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: {BG_MAIN};
        height: 10px;
        margin: 0px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: #3e3e50;
        min-width: 20px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {ACCENT_COLOR};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
        width: 0px;
    }}
    
    /* Group Boxes */
    QGroupBox {{
        border: 1px solid {BORDER_COLOR};
        border-radius: 8px;
        margin-top: 1.5ex;
        font-weight: bold;
        color: {ACCENT_COLOR};
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
    }}
    
    /* List View / Tree View */
    QListView, QTreeView {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_COLOR};
        border-radius: 6px;
        padding: 4px;
        selection-background-color: rgba(0, 240, 255, 0.15);
        selection-color: {TEXT_PRIMARY};
    }}
    
    QListView::item, QTreeView::item {{
        padding: 6px 8px;
        border-radius: 4px;
    }}
    
    QListView::item:hover, QTreeView::item:hover {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    QListView::item:selected, QTreeView::item:selected {{
        background-color: rgba(0, 240, 255, 0.2);
        color: {TEXT_PRIMARY};
        font-weight: bold;
    }}
    
    /* ToolTip */
    QToolTip {{
        background-color: {BG_CARD};
        color: {TEXT_PRIMARY};
        border: 1px solid {ACCENT_COLOR};
        border-radius: 4px;
        padding: 4px;
    }}
    
    /* Progress Bar */
    QProgressBar {{
        background-color: {BG_INPUT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 4px;
        text-align: center;
        color: {TEXT_PRIMARY};
        font-weight: bold;
    }}
    
    QProgressBar::chunk {{
        background-color: {ACCENT_COLOR};
        border-radius: 3px;
    }}
    """
