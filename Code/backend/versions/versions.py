"""
Version History Logic

Provides:
- init_db(db_path)
- save_version(...)
- get_version_history(session_id)
- get_version(version_id)
- generate_diff(old, new)

Notes:
- SQLite-based persistence
- JSON-safe storage
- Git-like version chaining
"""

import sqlite3
import json
import os
from datetime import datetime
import difflib
from typing import Optional, Any, Tuple

DEFAULT_DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database", "versions.db")
)

# ---------------------------
# Database helpers
# ---------------------------

def get_conn(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialize DB schema (call explicitly from app startup)."""
    conn = get_conn(db_path)
    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_sessions (
                id TEXT PRIMARY KEY,
                filename TEXT,
                created_at TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS version_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                parent_id INTEGER,
                original_code TEXT,
                refactored_code TEXT,
                diff TEXT,
                diff_summary TEXT,
                issues TEXT,
                complexity TEXT,
                quality_score INTEGER,
                created_at TEXT,
                FOREIGN KEY(session_id) REFERENCES code_sessions(id),
                FOREIGN KEY(parent_id) REFERENCES version_history(id)
            )
        """)

        conn.commit()
    finally:
        conn.close()


# ---------------------------
# Utility helpers
# ---------------------------

def iso_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _json_dumps_safe(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return json.dumps(str(obj))


def _json_loads_safe(value: Optional[str]) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return value


# ---------------------------
# Diff generation
# ---------------------------

def generate_diff(old_code: str, new_code: str) -> Tuple[str, str]:
    old_code = old_code or ""
    new_code = new_code or ""

    if old_code == new_code:
        return "", ""

    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)

    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="original.py",
            tofile="refactored.py",
            lineterm=""
        )
    )

    diff_text = "\n".join(diff_lines)

    additions = sum(1 for ln in diff_lines if ln.startswith("+") and not ln.startswith("+++"))
    deletions = sum(1 for ln in diff_lines if ln.startswith("-") and not ln.startswith("---"))

    summary = []
    if additions:
        summary.append(f"{additions} additions")
    if deletions:
        summary.append(f"{deletions} deletions")

    return diff_text, ", ".join(summary) if summary else "modified"


# ---------------------------
# Core API
# ---------------------------

def save_version(
    session_id: str,
    original_code: str,
    issues: Any,
    complexity: Any,
    qualityScore: Optional[int],
    refactored_code: Optional[str] = None,
    diff: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH,
) -> dict:
    """Save a Git-like version snapshot."""

    refactored_code = refactored_code or original_code

    conn = get_conn(db_path)
    try:
        cur = conn.cursor()

        # Ensure session exists
        cur.execute("SELECT id FROM code_sessions WHERE id = ?", (session_id,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO code_sessions (id, filename, created_at) VALUES (?, ?, ?)",
                (session_id, None, iso_now())
            )

        # Find parent version
        cur.execute("""
            SELECT id FROM version_history
            WHERE session_id = ?
            ORDER BY datetime(created_at) DESC
            LIMIT 1
        """, (session_id,))
        parent = cur.fetchone()
        parent_id = parent["id"] if parent else None

        # Diff handling
        if original_code == refactored_code:
            diff_text, diff_summary = "", ""
        elif diff is not None:
            diff_text = diff
            _, diff_summary = generate_diff(original_code, refactored_code)
        else:
            diff_text, diff_summary = generate_diff(original_code, refactored_code)

        created_at = iso_now()

        cur.execute("""
            INSERT INTO version_history (
                session_id, parent_id,
                original_code, refactored_code,
                diff, diff_summary,
                issues, complexity,
                quality_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            parent_id,
            original_code,
            refactored_code,
            diff_text,
            diff_summary,
            _json_dumps_safe(issues),
            _json_dumps_safe(complexity),
            qualityScore,
            created_at,
        ))

        conn.commit()
        return {"ok": True, "version_id": cur.lastrowid, "parent_id": parent_id, "created_at": created_at}

    except sqlite3.DatabaseError as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}

    finally:
        conn.close()


def get_version_history(session_id: str, db_path: str = DEFAULT_DB_PATH) -> dict:
    conn = get_conn(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, parent_id, created_at, diff_summary
            FROM version_history
            WHERE session_id = ?
            ORDER BY datetime(created_at) ASC
        """, (session_id,))

        history = [{
            "version_id": r["id"],
            "parent_id": r["parent_id"],
            "created_at": r["created_at"],
            "summary": r["diff_summary"] or "Snapshot",
            "diff_summary": r["diff_summary"] or "",
        } for r in cur.fetchall()]

        return {"ok": True, "history": history}

    except sqlite3.DatabaseError as e:
        return {"ok": False, "error": str(e)}

    finally:
        conn.close()


def get_version(version_id: int, db_path: str = DEFAULT_DB_PATH) -> dict:
    conn = get_conn(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM version_history WHERE id = ?", (version_id,))
        row = cur.fetchone()

        if not row:
            return {"ok": False, "error": "Version not found"}

        return {
            "ok": True,
            "version": {
                "id": row["id"],
                "session_id": row["session_id"],
                "parent_id": row["parent_id"],
                "original_code": row["original_code"],
                "refactored_code": row["refactored_code"],
                "diff": row["diff"] or "",
                "diff_summary": row["diff_summary"] or "",
                "issues": _json_loads_safe(row["issues"]),
                "complexity": _json_loads_safe(row["complexity"]),
                "qualityScore": row["quality_score"],
                "created_at": row["created_at"],
            },
        }

    except sqlite3.DatabaseError as e:
        return {"ok": False, "error": str(e)}

    finally:
        conn.close()


def delete_version(version_id: int, db_path: str = DEFAULT_DB_PATH) -> dict:
    conn = get_conn(db_path)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM version_history WHERE id = ?", (version_id,))
        conn.commit()
        return {"ok": True}
    except sqlite3.DatabaseError as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()


def clear_versions(session_id: str, db_path: str = DEFAULT_DB_PATH) -> dict:
    conn = get_conn(db_path)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM version_history WHERE session_id = ?", (session_id,))
        conn.commit()
        return {"ok": True}
    except sqlite3.DatabaseError as e:
        return {"ok": False, "error": str(e)}
    finally:
        conn.close()
