from functools import wraps
from flask import session
import os
import re
import pymysql
from contextlib import contextmanager

db_config = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASS", "sqlpasswordsql"),
    "db": os.environ.get("DB_NAME", "sql_db"),
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


@contextmanager
def get_sql_db_connection():
    conn = pymysql.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()


def sql(query, args=""):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            if args:
                cur.execute(query, args)
            else:
                cur.execute(query)
            return cur.fetchall()


# Custom decorator for checking user roles
def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if user is logged in and user_role is in session
            if "user" not in session or "type" not in session["user"]:
                return "Unauthorized 1", 403
            # Check if user has at least one of the required roles
            user_type = session["user"]["type"]
            if user_type not in roles:
                return "Unauthorized 2", 403
            # User has required role, proceed to the route function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    special_characters = '!@#$%^&*(),.?":{}|<>'
    if not any(char in special_characters for char in password):
        return False, "Password must contain at least one special character"
    return True, "Password meets complexity requirements"


def check_email(email):
    # Regular expression pattern for validating email addresses
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(pattern, email):
        return True
    else:
        return False


def getproblemset_id(lecture_id, lecture_problemsetid):
    problemset_id = sql(
        "SELECT problemset_id FROM problemsets WHERE lecture_id=%s AND lecture_problemsetid=%s",
        (lecture_id, lecture_problemsetid),
    )

    return problemset_id[-1]["problemset_id"]


def getproblem_id(lecture_id, lecture_problemsetid, problemset_problemid):
    problemset_id = sql(
        "SELECT problemset_id FROM problemsets WHERE lecture_id=%s AND lecture_problemsetid=%s",
        (lecture_id, lecture_problemsetid),
    )[-1]["problemset_id"]
    problem_id = sql(
        "SELECT problem_id FROM problems WHERE problemset_id=%s AND problemset_problemid=%s",
        (problemset_id, problemset_problemid),
    )

    return problem_id[-1]["problem_id"]
