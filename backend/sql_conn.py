import os
import pymysql
from contextlib import contextmanager

db_config = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "sqlpasswordsql"),
    "db": os.environ.get("DB_NAME", "sql_db"),
    "port": 3306,
    "autocommit": True
}

@contextmanager
def get_sql_db_connection():
    conn = pymysql.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()