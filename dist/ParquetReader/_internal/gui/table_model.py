from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
import pyarrow as pa
from typing import Any, Optional, List

class PyArrowTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.table: Optional[pa.Table] = None
        self.columns: List[str] = []
        self.cached_data: List[List[Any]] = [] # Fast local Python list cache
        
        # Muted lavender color cached statically to avoid repeated instantiations
        self.null_color = QColor("#6272a4")
        
    def setTable(self, table: Optional[pa.Table]):
        """
        Registers a new PyArrow Table or Table slice to render inside the view.
        Converts PyArrow columns to native Python lists instantly in C++ for extreme performance.
        """
        self.beginResetModel()
        self.table = table
        if table is not None:
            self.columns = table.column_names
            # Fast batch conversion of columns to native Python lists
            self.cached_data = [col.to_pylist() for col in table.columns]
        else:
            self.columns = []
            self.cached_data = []
        self.endResetModel()
        
    def rowCount(self, parent=None) -> int:
        if not self.cached_data:
            return 0
        return len(self.cached_data[0])
        
    def columnCount(self, parent=None) -> int:
        return len(self.columns)
        
    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not self.cached_data:
            return None
            
        row = index.row()
        col = index.column()
        
        # Out-of-bounds protection
        if col >= len(self.cached_data) or row >= len(self.cached_data[col]):
            return None
            
        val = self.cached_data[col][row]
        
        # Display role: formats dates, round floats and dims nulls
        if role == Qt.ItemDataRole.DisplayRole:
            if val is None:
                return "<null>"
            if isinstance(val, float):
                return f"{val:,.2f}"
            if isinstance(val, int) and not isinstance(val, bool):
                return f"{val:,}"
            return str(val)
            
        # Text alignment role: right-align numbers, left-align others
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            
        # Foreground role: paint null values with muted color
        elif role == Qt.ItemDataRole.ForegroundRole:
            if val is None:
                return self.null_color
                
        return None
        
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
            
        if orientation == Qt.Orientation.Horizontal:
            if 0 <= section < len(self.columns):
                return self.columns[section]
        else:
            return f"{section + 1:,}"
        return None
