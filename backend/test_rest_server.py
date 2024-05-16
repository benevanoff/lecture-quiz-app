import random
import string
import pytest
import requests

from rest_server import app
from helper import sql

SERVER_URL = "http://127.0.0.1:8080"
USERNAME = "test_username"

VALID_DATA = {
    "name": "Rizu Student",
    "username": USERNAME,
    "email": "rizustudent@gmail.com",
    "password": "Password&123123",
    "type": "admin",
}

OLD_CREDENTIALS = {"username": USERNAME, "password": "Password&123123"}

VALID_CREDENTIALS = {"username": USERNAME, "password": "Password&123123"}

UPDATED_PROFILE_DATA = {"name": "Updated Name", "email": "updated@example.com"}

RESET_PASSWORD_DATA = {
    "old_password": "Password&123123",
    "new_password": "Password$123123",
}

LECTURE_DATA = {
    "title": "Introduction to Python",
    "body": "This is an introductory lecture to Python programming language.",
    "category": "technology",
}

UPDATED_LECTURE_DATA = {
    "title": "Updated Introduction to Python",
    "body": "This is an updated introductory lecture to Python programming language.",
    "category": "technology",
}

PROBLEM_SET_DATA = {
    "title": "Problem Set 1",
    "body": "This is the first problem set for the Introduction to Python lecture.",
}

UPDATED_PROBLEM_SET_DATA = {
    "title": "Updated Problem Set 1",
    "body": "This is an updated problem set for the Introduction to Python lecture.",
}

PROBLEM_DATA = {
    "title": "Math Quiz",
    "question": "What is the result of 2 + 2?",
    "option1": "2",
    "option2": "3",
    "option3": "4",
    "option4": "5",
    "correct": "4",
}

UPDATED_PROBLEM_DATA = {
    "title": "Math Quiz",
    "question": "What is the result of 2 + 3?",
    "option1": "2",
    "option2": "3",
    "option3": "4",
    "option4": "5",
    "correct": "5",
}


@pytest.fixture
def server_url():
    return SERVER_URL


def clear_database():
    sql("DELETE FROM lectures")
    sql("DELETE FROM problems")
    sql("DELETE FROM problemsets")
    sql("DELETE FROM users")


def create_test_user():
    sql("DELETE FROM users WHERE username=%s", (USERNAME))
    with requests.Session() as session:
        # Register
        response = session.post(f"{SERVER_URL}/register", json=VALID_DATA)
        assert response.status_code == 200


def test_root_endpoint(server_url):
    response = requests.get(f"{server_url}/")
    assert response.status_code == 200
    assert response.text == "Welcome to Lecture Quiz App!"


def test_user_register_login_update_reset(server_url):
    sql("DELETE FROM users WHERE username=%s", (USERNAME))
    with requests.Session() as session:
        # Register
        response = session.post(f"{server_url}/register", json=VALID_DATA)
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Login
        response = session.post(f"{server_url}/login", json=OLD_CREDENTIALS)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Update profile
        response = session.post(
            f"{server_url}/profile/update", json=UPDATED_PROFILE_DATA
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Reset password
        response = session.post(
            f"{server_url}/reset_password", json=RESET_PASSWORD_DATA
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Logout
        response = requests.post(f"{server_url}/logout")
        assert response.status_code == 200
        assert response.json()["completed"] == True


def test_lectures_and_problem_sets_get_create(server_url):
    clear_database
    create_test_user()
    with requests.Session() as session:
        # Login
        response = session.post(f"{server_url}/login", json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Create lecture
        response = session.post(f"{server_url}/lecture/create", json=LECTURE_DATA)
        assert response.status_code == 200
        assert response.json()["completed"] == True
        test_lecture_id = response.json()["lecture_id"]

        # Get the created lecture
        response = session.get(f"{server_url}/l{test_lecture_id}")
        assert response.status_code == 200
        lecture_data = response.json()
        assert lecture_data["title"] == "Introduction to Python"
        assert lecture_data["category"] == "technology"

        # Create problem set under the created lecture
        response = session.post(
            f"{server_url}/l{test_lecture_id}/problemset/create", json=PROBLEM_SET_DATA
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True
        test_problemset_id = response.json()["lecture_problemsetid"]

        # Get list of problem sets for the lecture
        response = session.get(
            f"{server_url}/l{test_lecture_id}/problemsets", json=PROBLEM_SET_DATA
        )
        assert response.status_code == 200
        assert len(response.text) > 0

        # Create problem under the created problem set
        response = session.post(
            f"{server_url}/l{test_lecture_id}/ps{test_problemset_id}/problem/create",
            json=PROBLEM_DATA,
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True
        test_problem_id = response.json()["problemset_problemid"]

        # Edit the lecture
        response = session.post(
            f"{server_url}/l{test_lecture_id}/edit", json=UPDATED_LECTURE_DATA
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Edit the problem set
        response = session.post(
            f"{server_url}/l{test_lecture_id}/ps{test_problemset_id}/edit",
            json=UPDATED_PROBLEM_SET_DATA,
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Edit the problem
        response = session.post(
            f"{server_url}/l{test_lecture_id}/ps{test_problemset_id}/p{test_problem_id}/edit",
            json=UPDATED_PROBLEM_DATA,
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Delete the problem
        response = session.post(
            f"{server_url}/l{test_lecture_id}/ps{test_problemset_id}/p{test_problem_id}/delete"
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Delete the problem set
        response = session.post(
            f"{server_url}/l{test_lecture_id}/ps{test_problemset_id}/delete"
        )
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Delete the lecture
        response = session.post(f"{server_url}/l{test_lecture_id}/delete")
        assert response.status_code == 200
        assert response.json()["completed"] == True

def test_delete_account(server_url):
    clear_database
    create_test_user()
    with requests.Session() as session:
        # Login
        response = session.post(f"{server_url}/login", json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.json()["completed"] == True

        # Delete the profile
        response = session.post(f"{server_url}/account/delete", json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.json()["completed"] == True

if __name__ == "__main__":
    pytest.main()
