import json
import sqlite3

def init_db(path):
    with sqlite3.connect(path) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS analyses (id INTEGER PRIMARY KEY AUTOINCREMENT, target_role TEXT, score REAL, analysis_date TEXT, payload TEXT NOT NULL)')

def save_analysis(path, payload):
    with sqlite3.connect(path) as conn:
        cursor = conn.execute('INSERT INTO analyses (target_role, score, analysis_date, payload) VALUES (?, ?, ?, ?)', (payload['target_role'], payload['final_score'], payload['analysis_date'], json.dumps(payload)))
        return cursor.lastrowid

def list_analyses(path):
    with sqlite3.connect(path) as conn:
        rows = conn.execute('SELECT id, target_role, score, analysis_date FROM analyses ORDER BY id DESC').fetchall()
    return [{'id': row[0], 'target_role': row[1], 'score': row[2], 'analysis_date': row[3]} for row in rows]

def get_analysis(path, analysis_id):
    with sqlite3.connect(path) as conn:
        row = conn.execute('SELECT payload FROM analyses WHERE id = ?', (analysis_id,)).fetchone()
    return json.loads(row[0]) if row else None

def delete_analysis(path, analysis_id):
    with sqlite3.connect(path) as conn:
        cursor = conn.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
        return cursor.rowcount > 0
