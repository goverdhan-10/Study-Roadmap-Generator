import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path("analysis_results.db")

def _get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        file_path TEXT,
        analyzed_at TEXT,
        basic_concepts TEXT,
        advanced_concepts TEXT,
        prerequisites TEXT,
        roadmap TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_analysis(file_path: str, analysis: Dict[str, Any], analyzed_at: str = None):
    from datetime import datetime
    init_db()
    analyzed_at = analyzed_at or datetime.now().isoformat(timespec="seconds")
    file_name = Path(file_path).name
    with _get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO analyses (file_name, file_path, analyzed_at, basic_concepts, advanced_concepts, prerequisites, roadmap)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            file_name,
            file_path,
            analyzed_at,
            json.dumps(analysis.get("basic_concepts", []), ensure_ascii=False),
            json.dumps(analysis.get("advanced_concepts", []), ensure_ascii=False),
            json.dumps(analysis.get("prerequisite_concepts", []), ensure_ascii=False),
            json.dumps(analysis.get("roadmap", []), ensure_ascii=False)
        ))
        conn.commit()

def load_all_analyses(limit: int = 50) -> List[Dict[str, Any]]:
    init_db()
    with _get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT id, file_name, file_path, analyzed_at, basic_concepts, advanced_concepts, prerequisites, roadmap
        FROM analyses ORDER BY analyzed_at DESC LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
    out = []
    for r in rows:
        rid, file_name, file_path, analyzed_at, basic, adv, prereq, roadmap = r
        out.append({
            "id": rid,
            "file_name": file_name,
            "file_path": file_path,
            "analyzed_at": analyzed_at,
            "basic_concepts": json.loads(basic or "[]"),
            "advanced_concepts": json.loads(adv or "[]"),
            "prerequisite_concepts": json.loads(prereq or "[]"),
            "roadmap": json.loads(roadmap or "[]"),
        })
    return out  