import os
import pyarrow.parquet as pq
import pyarrow as pa
import json
from typing import Dict, Any, Tuple, Optional

class ParquetLoader:
    def __init__(self):
        self.filepath: Optional[str] = None
        self.table: Optional[pa.Table] = None
        self.metadata: Dict[str, Any] = {}
        
    def load_file(self, filepath: str) -> Tuple[bool, str]:
        """
        Loads a parquet file, extracts its metadata, and loads it into a pyarrow Table.
        """
        if not os.path.exists(filepath):
            return False, "File does not exist."
            
        try:
            self.filepath = filepath
            
            # Read schema and metadata using pyarrow
            # memory_map=True heavily speeds up reading large local files (zero-copy when possible)
            pf = pq.ParquetFile(filepath, memory_map=True)
            self.metadata = {
                "filename": os.path.basename(filepath),
                "filepath": filepath,
                "file_size_mb": round(os.path.getsize(filepath) / (1024 * 1024), 2),
                "row_count": pf.metadata.num_rows,
                "column_count": pf.metadata.num_columns,
                "row_groups": pf.metadata.num_row_groups,
                "serialized_size_kb": round(pf.metadata.serialized_size / 1024, 2),
                "format_version": pf.metadata.format_version,
                "creator": pf.metadata.created_by or "Unknown"
            }
            
            # Load PyArrow Table directly (super fast, no Pandas conversion!)
            self.table = pf.read()
            
            return True, "Success"
        except Exception as e:
            self.filepath = None
            self.table = None
            self.metadata = {}
            return False, f"Failed to read parquet file: {str(e)}"
            
    def export_data(self, table_to_export: pa.Table, format_type: str, save_path: str) -> Tuple[bool, str]:
        """
        Exports the provided PyArrow Table to the specified format.
        """
        if table_to_export is None:
            table_to_export = self.table
            
        if table_to_export is None:
            return False, "No data to export."
            
        try:
            if format_type == "csv":
                import pyarrow.csv as pc
                pc.write_csv(table_to_export, save_path)
            elif format_type == "parquet":
                pq.write_table(table_to_export, save_path)
            elif format_type == "json":
                # Limit to first 20,000 rows BEFORE converting to python dictionary 
                # to prevent massive memory spikes on large tables
                export_table = table_to_export.slice(0, 20000)
                
                pydict = export_table.to_pydict()
                keys = list(pydict.keys())
                num_rows = export_table.num_rows
                
                rows = []
                for i in range(num_rows):
                    row = {k: pydict[k][i] for k in keys}
                    rows.append(row)
                    
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(rows, f, ensure_ascii=False, indent=2)
            else:
                return False, f"Unsupported format: {format_type}"
            return True, "Success"
        except Exception as e:
            return False, str(e)
