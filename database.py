import sqlite3
import datetime

DB_PATH = "vaibrant.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        risk_level TEXT NOT NULL,
        lines_of_code INTEGER,
        analysis TEXT,
        imports TEXT,
        dangerous_calls TEXT,
        scanned_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

def save_scan(filename, risk_level, lines_of_code, analysis, imports, dangerous_calls):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans
        (filename, risk_level, lines_of_code, analysis, imports, dangerous_calls, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename, risk_level, lines_of_code, analysis, str(imports), str(dangerous_calls),
        datetime.datetime.now().isoformat()
        )
    )
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

def get_all_scans():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY scanned_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_scans_by_risk(risk_level):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM scans WHERE risk_level=? ORDER BY scanned_at DESC",
        (risk_level,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_scan_by_id (scan_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM scans WHERE id=?",
        (scan_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_scans_by_filename(filename):
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM scans WHERE filename=? ORDER BY scanned_at DESC",
        (filename,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

if __name__ == "__main__":
    init_db()
    print("Database ready")