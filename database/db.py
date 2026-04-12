import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            expiry TEXT NOT NULL,
            signature_hex TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_file(filename, file_hash, expiry, signature_hex):
    conn = get_db_connection()
    created_at = datetime.datetime.utcnow().isoformat()
    conn.execute('''
        INSERT INTO files (filename, file_hash, expiry, signature_hex, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, file_hash, expiry, signature_hex, created_at))
    conn.commit()
    conn.close()

def get_all_files():
    conn = get_db_connection()
    files = conn.execute('SELECT * FROM files ORDER BY id DESC').fetchall()
    conn.close()
    return [dict(ix) for ix in files]

def get_file_by_id(file_id):
    conn = get_db_connection()
    file_record = conn.execute('SELECT * FROM files WHERE id = ?', (file_id,)).fetchone()
    conn.close()
    if file_record:
        return dict(file_record)
    return None

def get_file_by_name(filename):
    conn = get_db_connection()
    # It's possible there are multiple uploads with the same name, we return the most recent
    file_record = conn.execute('SELECT * FROM files WHERE filename = ? ORDER BY id DESC', (filename,)).fetchone()
    conn.close()
    if file_record:
        return dict(file_record)
    return None
