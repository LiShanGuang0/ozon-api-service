from collections.abc import Iterable
from contextlib import contextmanager
from typing import Any

import pymysql
from pymysql.cursors import DictCursor

from app.core.config import get_settings


@contextmanager
def mysql_conn():
    settings = get_settings()
    conn = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(sql: str, params: Iterable[Any] | dict[str, Any] | None = None) -> dict[str, Any] | None:
    with mysql_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()


def fetch_all(sql: str, params: Iterable[Any] | dict[str, Any] | None = None) -> list[dict[str, Any]]:
    with mysql_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return list(cursor.fetchall())


def execute(sql: str, params: Iterable[Any] | dict[str, Any] | None = None) -> int:
    with mysql_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount


def execute_lastrowid(sql: str, params: Iterable[Any] | dict[str, Any] | None = None) -> int:
    with mysql_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return int(cursor.lastrowid)
