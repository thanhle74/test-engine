from flask import Blueprint, request, jsonify
from db import get_db_connection
from utils.rule_to_sql import build_sql_from_rule 
import os

user_bp = Blueprint("user", __name__)

@user_bp.route("/init-db", methods=["POST"])
def init_db_from_file():
    try:
        data = request.get_json()
        type_ = data.get("type")
        if type_ == "table":
            SQL_FILE = "db/create_table.sql"
        elif type_ == "data":
            SQL_FILE = "db/create_data.sql"
        else:
            return jsonify({"error": "Invalid type"}), 400

        with open(SQL_FILE, "r") as f:
            sql = f.read()
        conn = get_db_connection()
        conn.executescript(sql)
        conn.commit()
        conn.close()
        return jsonify({"message": f"✅ SQL `{type_}` executed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route("/generate-sql", methods=["POST"])
def generate_sql():
    try:
        rule_json = request.get_json()

        # Lấy page & page_size (nếu có)
        page = int(rule_json.get("page", 1))
        page_size = int(rule_json.get("page_size", 10))
        offset = (page - 1) * page_size

        # Tạo SQL từ rule
        base_sql = build_sql_from_rule(rule_json)

        # Câu query có LIMIT để phân trang
        paginated_sql = f"{base_sql[:-1]} LIMIT {page_size} OFFSET {offset};"

        conn = get_db_connection()
        cursor = conn.cursor()

        # Truy vấn dữ liệu phân trang
        cursor.execute(paginated_sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        # Truy vấn tổng số dòng (total)
        count_sql = f"SELECT COUNT(*) FROM ({base_sql[:-1]}) as count_subquery;"
        cursor.execute(count_sql)
        total = cursor.fetchone()[0]
        total_pages = (total + page_size - 1) // page_size

        conn.close()

        return jsonify({
            "sql": base_sql,
            "results": results,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
