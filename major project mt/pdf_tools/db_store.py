from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = Path("analysis_results.db")


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db() -> None:
    
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
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
        """
    )
    conn.commit()
    conn.close()


def save_analysis(file_path: str, analysis: Dict[str, Any]) -> None:
    
    from datetime import datetime

    init_db()

    file_name = Path(file_path).name
    analyzed_at = datetime.now().isoformat(timespec="seconds")

    basic = json.dumps(analysis.get("basic_concepts", []), ensure_ascii=False)
    advanced = json.dumps(analysis.get("advanced_concepts", []), ensure_ascii=False)
    prereq = json.dumps(analysis.get("prerequisite_concepts", []), ensure_ascii=False)
    roadmap = json.dumps(analysis.get("roadmap", []), ensure_ascii=False)

    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO analyses (
            file_name, file_path, analyzed_at,
            basic_concepts, advanced_concepts, prerequisites, roadmap
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (file_name, file_path, analyzed_at, basic, advanced, prereq, roadmap),
    )
    conn.commit()
    conn.close()


def load_all_analyses(limit: int = 50) -> List[Dict[str, Any]]:
    
    init_db()
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id, file_name, file_path, analyzed_at,
            basic_concepts, advanced_concepts, prerequisites, roadmap
        FROM analyses
        ORDER BY analyzed_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    out: List[Dict[str, Any]] = []
    for row in rows:
        (
            rid,
            file_name,
            file_path,
            analyzed_at,
            basic_json,
            adv_json,
            prereq_json,
            roadmap_json,
        ) = row

        out.append(
            {
                "id": rid,
                "file_name": file_name,
                "file_path": file_path,
                "analyzed_at": analyzed_at,
                "basic_concepts": json.loads(basic_json or "[]"),
                "advanced_concepts": json.loads(adv_json or "[]"),
                "prerequisite_concepts": json.loads(prereq_json or "[]"),
                "roadmap": json.loads(roadmap_json or "[]"),
            }
        )
    return out
