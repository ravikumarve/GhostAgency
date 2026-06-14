"""SQLite-backed persistent settings store.

Reads from DB with env var fallback. Writes go to DB only.
Settings are immediately visible to the app at runtime.
"""

from __future__ import annotations

import os
import sqlite3
import threading

from ghostagency.core.config import LOG_DIR

DB_DIR = LOG_DIR.parent / "data"
DB_PATH = DB_DIR / "settings.db"

_local = threading.local()


def _get_conn() -> sqlite3.Connection:
    """Get thread-local connection."""
    if not hasattr(_local, "conn") or _local.conn is None:
        DB_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        _init_table(conn)
        _local.conn = conn
    return _local.conn


def _init_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get(key: str, default: str | None = None) -> str | None:
    """Get a setting from DB. Falls back to env var, then default."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?", (key,)
    ).fetchone()
    if row is not None:
        return row["value"]
    # Fallback to env var
    env_val = os.getenv(key.upper())
    if env_val is not None:
        return env_val
    return default


def get_int(key: str, default: int = 0) -> int:
    """Get a setting as int."""
    val = get(key)
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def get_bool(key: str, default: bool = False) -> bool:
    """Get a setting as bool."""
    val = get(key)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes")


def set(key: str, value: str) -> None:
    """Set a setting in the DB."""
    conn = _get_conn()
    conn.execute(
        """INSERT INTO settings (key, value, updated_at)
           VALUES (?, ?, CURRENT_TIMESTAMP)
           ON CONFLICT(key) DO UPDATE SET
               value = excluded.value,
               updated_at = CURRENT_TIMESTAMP""",
        (key, value),
    )
    conn.commit()


def set_many(items: dict[str, str]) -> None:
    """Set multiple settings in a single transaction."""
    conn = _get_conn()
    conn.execute("BEGIN")
    try:
        for key, value in items.items():
            conn.execute(
                """INSERT INTO settings (key, value, updated_at)
                   VALUES (?, ?, CURRENT_TIMESTAMP)
                   ON CONFLICT(key) DO UPDATE SET
                       value = excluded.value,
                       updated_at = CURRENT_TIMESTAMP""",
                (key, value),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_all() -> dict[str, str]:
    """Return all stored settings (keys lowercase)."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT key, value FROM settings ORDER BY key"
    ).fetchall()
    return {row["key"]: row["value"] for row in rows}


def get_by_prefix(prefix: str) -> dict[str, str]:
    """Return settings whose key starts with a prefix."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT key, value FROM settings WHERE key LIKE ? ORDER BY key",
        (f"{prefix}%",),
    ).fetchall()
    return {row["key"]: row["value"] for row in rows}


def delete(key: str) -> None:
    """Remove a setting (reverts to env var fallback)."""
    conn = _get_conn()
    conn.execute("DELETE FROM settings WHERE key = ?", (key,))
    conn.commit()


def clear() -> None:
    """Remove all settings (reverts entirely to env vars)."""
    conn = _get_conn()
    conn.execute("DELETE FROM settings")
    conn.commit()


def get_effective(prefix: str = "") -> dict[str, str]:
    """Merge DB settings + relevant env vars (DB wins)."""
    result: dict[str, str] = {}

    # Collect matching env vars
    for env_key, env_val in sorted(os.environ.items()):
        lkey = env_key.lower()
        if prefix and not lkey.startswith(prefix.lower()):
            continue
        result[lkey] = env_val

    # DB overrides
    db_overrides = get_by_prefix(prefix)
    result.update(db_overrides)

    return result
