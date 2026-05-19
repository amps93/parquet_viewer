from PySide6.QtCore import QAbstractTableModel, Qt
import pyarrow as pa
from typing import Any, Optional, List

class PyArrowTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.table: Optional[pa.Table] = None
        self.columns: List[str] = []
        
    def setTable(self, table: Optional[pa.Table]):
        """
        Registers a new PyArrow Table or Table slice to render inside the view.
        """
        self.beginResetModel()
        self.table = table
        if table is not None:
            self.columns = table.column_names
        else:
            self.columns = []
        self.endResetModel()
        
    def rowCount(self, parent=None) -> int:
        if self.table is None:
            return 0
        return self.table.num_rows
        
    def columnCount(self, parent=None) -> int:
        return len(self.columns)
        
    def data(self, index, role=Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or self.table is None:
            return None
            
        row = index.row()
        col = index.column()
        
        # Display role: formats dates, round floats and dims nulls
        if role == Qt.ItemDataRole.DisplayRole:
            val = self.table.column(col)[row].as_py()
            if val is None:
                return "<null>"
            if isinstance(val, float):
                return f"{val:,.2f}"
            if isinstance(val, int) and not isinstance(val, bool):
                return f"{val:,}"
            return str(val)
            
        # Text alignment role: right-align numbers, left-align others
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            val = self.table.column(col)[row].as_py()
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            
        # Foreground role: paint null values with muted color
        elif role == Qt.ItemDataRole.ForegroundRole:
            val = self.table.column(col)[row].as_py()
            if val is None:
                from PySide6.QtGui import QColor
                return QColor("#6272a4") # Muted lavender
                
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
