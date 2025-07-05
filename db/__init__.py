import sqlite3
import re

def get_db_connection():
    conn = sqlite3.connect("db/data.db")
    conn.row_factory = sqlite3.Row

    # ✅ Tạo hàm REGEXP
    def regexp(expr, item):
        if item is None:
            return False
        return re.search(expr, str(item)) is not None

    conn.create_function("REGEXP", 2, regexp)

    return conn
