import os
import sys
from typing import List, Optional
import pyarrow as pa
import pyarrow.compute as pc

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTableView, QFileDialog, 
                             QMessageBox, QSplitter, QListWidget, QComboBox, 
                             QLineEdit, QGroupBox)
from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtGui import QCursor

# Internal Imports
from gui.table_model import PyArrowTableModel
from gui.styling import Theme
from utils.parquet_loader import ParquetLoader

class ParquetViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Core engines
        self.loader = ParquetLoader()
        
        # State variables
        self.filtered_table: Optional[pa.Table] = None
        self.current_page = 0
        self.page_size = 500
        
        # Recent files settings
        self.settings = QSettings("Antigravity", "ParquetViewer")
        self.recent_files: List[str] = self.settings.value("recent_files", []) or []
        # Clean invalid recent files
        self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        
        # Theme configuration (persist last active theme)
        self.is_dark_mode = self.settings.value("is_dark_mode", True, type=bool)
        
        self.init_ui()
        self.apply_theme()
        self.update_theme_button_ui()
        
    def init_ui(self):
        self.setWindowTitle("Antigravity Parquet View Studio (Lightweight)")
        self.resize(1100, 700)
        self.setAcceptDrops(True)
        
        # Set Window and Taskbar Icon
        from PySide6.QtGui import QIcon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "parquet_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Main Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # --- Top Banner Header ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        title_container = QVBoxLayout()
        lbl_app_title = QLabel("⚡ Parquet View Studio")
        lbl_app_title.setObjectName("titleLabel")
        lbl_app_sub = QLabel("Lightweight High-Performance Parquet File Viewer")
        lbl_app_sub.setObjectName("subtitleLabel")
        title_container.addWidget(lbl_app_title)
        title_container.addWidget(lbl_app_sub)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # Header Actions
        self.btn_open = QPushButton("Open Parquet File")
        self.btn_open.setObjectName("primaryButton")
        self.btn_open.clicked.connect(self.select_and_open_file)
        header_layout.addWidget(self.btn_open)
        
        self.btn_gen_sample = QPushButton("Generate Sample Data")
        self.btn_gen_sample.clicked.connect(self.create_and_load_sample)
        header_layout.addWidget(self.btn_gen_sample)
        
        self.btn_theme_toggle = QPushButton("🌙 Night Mode")
        self.btn_theme_toggle.setToolTip("Toggle Light/Night Mode")
        self.btn_theme_toggle.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.btn_theme_toggle)
        
        self.btn_help = QPushButton("?")
        self.btn_help.setToolTip("Show Help & Documentation")
        self.btn_help.setFixedWidth(30)
        self.btn_help.clicked.connect(self.show_help)
        header_layout.addWidget(self.btn_help)
        
        main_layout.addLayout(header_layout)
        
        # --- Main Splitter (Sidebar + Data Grid Pane) ---
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # 1. Sidebar Container
        sidebar = QWidget()
        sidebar.setObjectName("sidebarFrame")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(12)
        
        # Sidebar Section A: Active File Metadata Card
        meta_group = QGroupBox("Active File Info")
        meta_layout = QVBoxLayout(meta_group)
        meta_layout.setSpacing(6)
        
        self.lbl_meta_name = QLabel("No file loaded")
        self.lbl_meta_name.setObjectName("metaFileName")
        self.lbl_meta_name.setWordWrap(True)
        
        self.lbl_meta_size = QLabel("Size: --")
        self.lbl_meta_rows = QLabel("Rows: --")
        self.lbl_meta_cols = QLabel("Columns: --")
        self.lbl_meta_ver = QLabel("Parquet Version: --")
        
        meta_layout.addWidget(self.lbl_meta_name)
        meta_layout.addWidget(self.lbl_meta_size)
        meta_layout.addWidget(self.lbl_meta_rows)
        meta_layout.addWidget(self.lbl_meta_cols)
        meta_layout.addWidget(self.lbl_meta_ver)
        sidebar_layout.addWidget(meta_group)
        
        # Sidebar Section B: Recent Files List
        recent_group = QGroupBox("Recent Files")
        recent_layout = QVBoxLayout(recent_group)
        self.list_recent = QListWidget()
        self.list_recent.setStyleSheet("font-size: 11px;")
        self.list_recent.itemDoubleClicked.connect(self.open_recent_file)
        self.update_recent_list_ui()
        recent_layout.addWidget(self.list_recent)
        
        # Clear recent button
        btn_clear_recent = QPushButton("Clear History")
        btn_clear_recent.setStyleSheet("font-size: 10px; padding: 2px 5px;")
        btn_clear_recent.clicked.connect(self.clear_recent_files)
        recent_layout.addWidget(btn_clear_recent)
        
        sidebar_layout.addWidget(recent_group)
        sidebar_layout.addStretch()
        
        # 2. Main Data Grid Pane
        grid_pane = QWidget()
        grid_layout = QVBoxLayout(grid_pane)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(8)
        
        # Filter Constructor Panel
        filter_group = QGroupBox("Fast Filter")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(10, 8, 10, 8)
        filter_layout.setSpacing(8)
        
        self.cb_filter_col = QComboBox()
        self.cb_filter_col.setPlaceholderText("Select Column")
        self.cb_filter_col.setFixedWidth(160)
        filter_layout.addWidget(self.cb_filter_col)
        
        self.cb_filter_op = QComboBox()
        self.cb_filter_op.addItems(["contains", "==", "!=", ">", "<", "starts with", "ends with"])
        self.cb_filter_op.setFixedWidth(110)
        filter_layout.addWidget(self.cb_filter_op)
        
        self.txt_filter_val = QLineEdit()
        self.txt_filter_val.setPlaceholderText("Filter criteria...")
        self.txt_filter_val.returnPressed.connect(self.apply_fast_filter)
        filter_layout.addWidget(self.txt_filter_val)
        
        self.btn_apply_filter = QPushButton("Apply Filter")
        self.btn_apply_filter.clicked.connect(self.apply_fast_filter)
        filter_layout.addWidget(self.btn_apply_filter)
        
        self.btn_reset_filter = QPushButton("Reset")
        self.btn_reset_filter.clicked.connect(self.reset_fast_filter)
        filter_layout.addWidget(self.btn_reset_filter)
        
        grid_layout.addWidget(filter_group)
        
        # Grid Table View
        self.tbl_grid = QTableView()
        self.tbl_grid.setAlternatingRowColors(True)
        self.grid_model = PyArrowTableModel()
        self.tbl_grid.setModel(self.grid_model)
        grid_layout.addWidget(self.tbl_grid)
        
        # Pagination & Actions Footer
        pagination_layout = QHBoxLayout()
        
        self.btn_export_grid = QPushButton("Export Dataset...")
        self.btn_export_grid.clicked.connect(self.export_current_dataset)
        self.btn_export_grid.setEnabled(False)
        pagination_layout.addWidget(self.btn_export_grid)
        
        pagination_layout.addStretch()
        
        # Pagination controls
        self.btn_page_first = QPushButton("|<")
        self.btn_page_first.setObjectName("navButton")
        self.btn_page_first.setToolTip("First Page")
        self.btn_page_first.setFixedWidth(32)
        self.btn_page_first.clicked.connect(self.page_first)
        pagination_layout.addWidget(self.btn_page_first)
        
        self.btn_page_prev = QPushButton("<")
        self.btn_page_prev.setObjectName("navButton")
        self.btn_page_prev.setToolTip("Previous Page")
        self.btn_page_prev.setFixedWidth(32)
        self.btn_page_prev.clicked.connect(self.page_prev)
        pagination_layout.addWidget(self.btn_page_prev)
        
        self.lbl_pagination_info = QLabel("Page 0 of 0 (Showing 0 - 0 of 0 rows)")
        self.lbl_pagination_info.setObjectName("paginationInfo")
        pagination_layout.addWidget(self.lbl_pagination_info)
        
        self.btn_page_next = QPushButton(">")
        self.btn_page_next.setObjectName("navButton")
        self.btn_page_next.setToolTip("Next Page")
        self.btn_page_next.setFixedWidth(32)
        self.btn_page_next.clicked.connect(self.page_next)
        pagination_layout.addWidget(self.btn_page_next)
        
        self.btn_page_last = QPushButton(">|")
        self.btn_page_last.setObjectName("navButton")
        self.btn_page_last.setToolTip("Last Page")
        self.btn_page_last.setFixedWidth(32)
        self.btn_page_last.clicked.connect(self.page_last)
        pagination_layout.addWidget(self.btn_page_last)
        
        pagination_layout.addSpacing(10)
        
        # Page size combobox
        pagination_layout.addWidget(QLabel("Page Size:"))
        self.cb_page_size = QComboBox()
        self.cb_page_size.addItems(["100", "250", "500", "1000", "2000"])
        self.cb_page_size.setCurrentText("500")
        self.cb_page_size.currentTextChanged.connect(self.change_page_size)
        self.cb_page_size.setFixedWidth(80)
        pagination_layout.addWidget(self.cb_page_size)
        
        grid_layout.addLayout(pagination_layout)
        
        # Add to main splitter
        main_splitter.addWidget(sidebar)
        main_splitter.addWidget(grid_pane)
        main_splitter.setSizes([240, 860])
        
        # --- Footer Status Bar ---
        self.lbl_status_footer = QLabel("Ready. Please open a Parquet file to begin.")
        self.lbl_status_footer.setObjectName("statusFooter")
        main_layout.addWidget(self.lbl_status_footer)
        
    def apply_theme(self):
        self.setStyleSheet(Theme.get_style(self.is_dark_mode))
        
    def select_and_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Parquet File", "", "Parquet Files (*.parquet *.pq)"
        )
        if file_path:
            self.load_parquet_file(file_path)
            
    def load_parquet_file(self, file_path: str):
        self.lbl_status_footer.setText(f"Loading {os.path.basename(file_path)}...")
        
        # Force UI update
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.processEvents()
        
        success, msg = self.loader.load_file(file_path)
        
        if success:
            self.filtered_table = self.loader.table
            self.current_page = 0
            
            # Update recent files list
            self.add_recent_file(file_path)
            
            # Setup columns for the fast filter
            self.cb_filter_col.clear()
            self.cb_filter_col.addItems(self.loader.table.column_names)
            
            # Update UI Panels
            self.update_meta_sidebar()
            self.update_grid_view(resize_columns=True)
            
            self.btn_export_grid.setEnabled(True)
            self.lbl_status_footer.setText(f"Successfully loaded parquet file with {self.loader.metadata['row_count']:,} rows.")
        else:
            QMessageBox.critical(self, "Load Error", f"Failed to open parquet file:\n{msg}")
            self.lbl_status_footer.setText(f"Load Error: {msg}")
            
    def create_and_load_sample(self):
        """
        Generates sample mock e-commerce sales dataset and loads it automatically.
        """
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        workspace_dir = os.path.join(app_dir, "data")
        self.lbl_status_footer.setText("Generating mock dataset (10,000 rows)...")
        
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.processEvents()
        
        try:
            from utils.sample_generator import save_mock_parquet
            sample_path = save_mock_parquet(workspace_dir, 10000)
            self.load_parquet_file(sample_path)
            QMessageBox.information(
                self, "Sample Created", 
                f"Generated mock E-Commerce Sales dataset (10,000 rows) successfully using pure PyArrow!\n\nSaved to:\n{sample_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Sample Error", f"Failed to generate mock sales dataset:\n{str(e)}")
            self.lbl_status_footer.setText(f"Sample Generation Error: {str(e)}")
            
    def update_meta_sidebar(self):
        meta = self.loader.metadata
        if not meta:
            return
            
        self.lbl_meta_name.setText(meta['filename'])
        self.lbl_meta_size.setText(f"Size: {meta['file_size_mb']} MB")
        self.lbl_meta_rows.setText(f"Rows: {meta['row_count']:,}")
        self.lbl_meta_cols.setText(f"Columns: {meta['column_count']:,}")
        self.lbl_meta_ver.setText(f"Format Version: {meta['format_version']}")
        self.lbl_meta_name.setToolTip(meta['filepath'])
        
    def update_grid_view(self, resize_columns: bool = False):
        if self.filtered_table is None or self.filtered_table.num_rows == 0:
            self.grid_model.setTable(None)
            self.lbl_pagination_info.setText("Page 0 of 0 (Showing 0 - 0 of 0 rows)")
            return
            
        total_rows = self.filtered_table.num_rows
        total_pages = max(1, (total_rows + self.page_size - 1) // self.page_size)
        
        # Boundary validation
        if self.current_page >= total_pages:
            self.current_page = total_pages - 1
        if self.current_page < 0:
            self.current_page = 0
            
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, total_rows)
        
        # Slice PyArrow Table directly (zero-copy, instantaneous!)
        sliced_table = self.filtered_table.slice(start_idx, end_idx - start_idx)
        self.grid_model.setTable(sliced_table)
        
        # Auto-adjust column sizes only when requested (saves seconds of rendering lag!)
        if resize_columns:
            self.tbl_grid.resizeColumnsToContents()
            for col in range(len(sliced_table.column_names)):
                w = min(self.tbl_grid.columnWidth(col), 350)
                self.tbl_grid.setColumnWidth(col, max(w, 80))
            
        # Update Info text
        self.lbl_pagination_info.setText(
            f"Page {self.current_page + 1} of {total_pages} (Showing {start_idx + 1:,} - {end_idx:,} of {total_rows:,} rows)"
        )
        
        # Toggle page buttons
        self.btn_page_first.setEnabled(self.current_page > 0)
        self.btn_page_prev.setEnabled(self.current_page > 0)
        self.btn_page_next.setEnabled(self.current_page < total_pages - 1)
        self.btn_page_last.setEnabled(self.current_page < total_pages - 1)
        
    def apply_fast_filter(self):
        if self.loader.table is None:
            return
            
        col = self.cb_filter_col.currentText()
        op = self.cb_filter_op.currentText()
        val_str = self.txt_filter_val.text().strip()
        
        if not col or not val_str:
            self.reset_fast_filter()
            return
            
        try:
            column_data = self.loader.table.column(col)
            field = self.loader.table.schema.field(col)
            col_type = field.type
            
            # String conversions and smart comparison conversions using pyarrow.compute
            if op == "contains":
                mask = pc.match_substring(column_data, val_str, ignore_case=True)
            elif op == "starts with":
                mask = pc.starts_with(column_data, val_str, ignore_case=True)
            elif op == "ends with":
                mask = pc.ends_with(column_data, val_str, ignore_case=True)
            else:
                # Convert comparison value to match dtype
                if pa.types.is_integer(col_type) or pa.types.is_floating(col_type):
                    try:
                        val = float(val_str)
                        if pa.types.is_integer(col_type):
                            val = int(val)
                        scalar_val = pa.scalar(val, type=col_type)
                    except ValueError:
                        raise ValueError(f"Value '{val_str}' must be numeric to filter numeric column '{col}'.")
                elif pa.types.is_boolean(col_type):
                    val = val_str.lower() in ('true', '1', 't', 'y', 'yes')
                    scalar_val = pa.scalar(val)
                elif pa.types.is_timestamp(col_type) or pa.types.is_date(col_type):
                    from datetime import datetime
                    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%H:%M:%S"):
                        try:
                            dt = datetime.strptime(val_str, fmt)
                            scalar_val = pa.scalar(dt).cast(col_type)
                            break
                        except ValueError:
                            continue
                    else:
                        raise ValueError(f"Could not parse date string '{val_str}'. Use YYYY-MM-DD.")
                else:
                    scalar_val = pa.scalar(val_str)
                    
                if op == "==":
                    mask = pc.equal(column_data, scalar_val)
                elif op == "!=":
                    mask = pc.not_equal(column_data, scalar_val)
                elif op == ">":
                    mask = pc.greater(column_data, scalar_val)
                elif op == "<":
                    mask = pc.less(column_data, scalar_val)
                else:
                    mask = pa.array([True] * self.loader.table.num_rows)
                    
            # Safe fill null values as False in comparison masks
            mask = pc.fill_null(mask, False)
            
            self.filtered_table = self.loader.table.filter(mask)
            self.current_page = 0
            self.update_grid_view(resize_columns=True)
            self.lbl_status_footer.setText(f"Filter applied. Returned {self.filtered_table.num_rows:,} matching rows.")
        except Exception as e:
            QMessageBox.critical(self, "Filter Error", f"Could not apply filter:\n{str(e)}")
            
    def reset_fast_filter(self):
        if self.loader.table is None:
            return
        self.txt_filter_val.clear()
        self.filtered_table = self.loader.table
        self.current_page = 0
        self.update_grid_view(resize_columns=True)
        self.lbl_status_footer.setText("Filter reset. Showing all rows.")
        
    def export_current_dataset(self):
        if self.filtered_table is None or self.filtered_table.num_rows == 0:
            QMessageBox.warning(self, "Empty Dataset", "There is no dataset to export.")
            return
            
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Explorer View", "", 
            "CSV Files (*.csv);;JSON Files (*.json);;Parquet Files (*.parquet)"
        )
        
        if not file_path:
            return
            
        fmt = "csv"
        if file_path.endswith(".json"):
            fmt = "json"
        elif file_path.endswith(".parquet"):
            fmt = "parquet"
            
        success, msg = self.loader.export_data(self.filtered_table, fmt, file_path)
        
        if success:
            QMessageBox.information(self, "Export Success", f"Successfully exported view dataset:\n{file_path}")
        else:
            QMessageBox.critical(self, "Export Failed", f"Could not export explorer view:\n{msg}")
            
    # --- Pagination Actions ---
    def page_first(self):
        self.current_page = 0
        self.update_grid_view()
        
    def page_prev(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_grid_view()
            
    def page_next(self):
        if self.filtered_table is not None:
            total_pages = (self.filtered_table.num_rows + self.page_size - 1) // self.page_size
            if self.current_page < total_pages - 1:
                self.current_page += 1
                self.update_grid_view()
                
    def page_last(self):
        if self.filtered_table is not None:
            total_pages = max(1, (self.filtered_table.num_rows + self.page_size - 1) // self.page_size)
            self.current_page = total_pages - 1
            self.update_grid_view()
            
    def change_page_size(self, size_str: str):
        try:
            self.page_size = int(size_str)
            self.current_page = 0
            self.update_grid_view(resize_columns=True)
        except ValueError:
            pass
            
    # --- Recent Files Cache Logic ---
    def add_recent_file(self, filepath: str):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.recent_files = self.recent_files[:8]
        
        self.settings.setValue("recent_files", self.recent_files)
        self.update_recent_list_ui()
        
    def update_recent_list_ui(self):
        self.list_recent.clear()
        for path in self.recent_files:
            base = os.path.basename(path)
            self.list_recent.addItem(base)
            items = self.list_recent.findItems(base, Qt.MatchFlag.MatchExactly)
            if items:
                items[0].setToolTip(path)
                
    def open_recent_file(self, item):
        path = item.toolTip()
        if os.path.exists(path):
            self.load_parquet_file(path)
        else:
            QMessageBox.warning(self, "File Not Found", f"The file no longer exists:\n{path}")
            if path in self.recent_files:
                self.recent_files.remove(path)
                self.settings.setValue("recent_files", self.recent_files)
                self.update_recent_list_ui()
                
    def clear_recent_files(self):
        self.recent_files.clear()
        self.settings.setValue("recent_files", [])
        self.list_recent.clear()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                if filepath.lower().endswith(('.parquet', '.pq')):
                    event.acceptProposedAction()
                    return
        event.ignore()
        
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                if filepath.lower().endswith(('.parquet', '.pq')):
                    self.load_parquet_file(filepath)
                    event.acceptProposedAction()
                    return
        event.ignore()
        
    def show_help(self):
        help_text = (
            "⚡ Antigravity Parquet View Studio (Lightweight) ⚡\n\n"
            "Features Summary:\n"
            "- Paginated grid view showing massive files (100 - 2000 rows per page).\n"
            "- Blazingly fast drag and drop or double-click to open.\n"
            "- Powerful fast filter with comparison operators (contains, ==, >, <, etc.)\n"
            "- Pure PyArrow-based, bypassing Pandas and NumPy completely for ultra-fast startup!\n"
            "- Native Windows system integration and recent files memory.\n\n"
            "System requirement: Python 3.8+ with PySide6 and PyArrow."
        )
        QMessageBox.information(self, "App Documentation", help_text)
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.settings.setValue("is_dark_mode", self.is_dark_mode)
        self.apply_theme()
        self.update_theme_button_ui()
        
    def update_theme_button_ui(self):
        if self.is_dark_mode:
            self.btn_theme_toggle.setText("🌙 Night Mode")
            self.btn_theme_toggle.setToolTip("Switch to Light Mode")
        else:
            self.btn_theme_toggle.setText("☀️ Light Mode")
            self.btn_theme_toggle.setToolTip("Switch to Night Mode")
