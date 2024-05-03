import random
import string
import pytest
import requests

from rest_server import app
from helper import sql

generate_username = lambda length=8: ''.join(random.choice(string.ascii_letters) for _ in range(length))

SERVER_URL = 'http://127.0.0.1:8080'
USERNAME = generate_username()

VALID_DATA = {
    "name": "Rizu Student",
    "username": USERNAME,
    "email": "rizustudent@gmail.com",
    "password": "Password&123123",
    "type": "admin"
}

OLD_CREDENTIALS = {
    "username": USERNAME,
    "password": "Password&123123"
}

VALID_CREDENTIALS = {
    "username": USERNAME,
    "password": "Password$123123"
}

UPDATED_PROFILE_DATA = {
    "name": "Updated Name",
    "email": "updated@example.com"
}

RESET_PASSWORD_DATA = {
    "old_password": "Password&123123",
    "new_password": "Password$123123"
}

LECTURE_DATA = {
    "title": "Introduction to Python",
    "body": "This is an introductory lecture to Python programming language.",
    "category": "technology"
}

UPDATED_LECTURE_DATA = {
    "title": "Updated Introduction to Python",
    "body": "This is an updated introductory lecture to Python programming language.",
    "category": "technology"
}

PROBLEM_SET_DATA = {
    "title": "Problem Set 1",
    "body": "This is the first problem set for the Introduction to Python lecture."
}

UPDATED_PROBLEM_SET_DATA = {
    "title": "Updated Problem Set 1",
    "body": "This is an updated problem set for the Introduction to Python lecture."
}

PROBLEM_DATA = {
    "title": "Math Quiz",
    "question": "What is the result of 2 + 2?",
    "option1": "2",
    "option2": "3",
    "option3": "4",
    "option4": "5",
    "correct": "4"
}

UPDATED_PROBLEM_DATA = {
    "title": "Math Quiz",
    "question": "What is the result of 2 + 3?",
    "option1": "2",
    "option2": "3",
    "option3": "4",
    "option4": "5",
    "correct": "5"
}

@pytest.fixture
def server_url():
    return SERVER_URL

def test_root_endpoint(server_url):
    response = requests.get(f'{server_url}/')
    assert response.status_code == 200
    assert response.text == "Welcome to Lecture Quiz App!"

def test_register_login_update_reset(server_url):
    with requests.Session() as session:
        # Register
        response = session.post(f'{server_url}/register', json=VALID_DATA)
        assert response.status_code == 200
        assert response.text == "Account made succesfully."

        # Login
        response = session.post(f'{server_url}/login', json=OLD_CREDENTIALS)
        print(response.text)
        assert response.status_code == 200
        assert response.text == "Logged In"

        # Update profile
        response = session.post(f'{server_url}/profile/update', json=UPDATED_PROFILE_DATA)
        assert response.status_code == 200
        assert response.text == "Profile updated successfully"

        # Reset password
        response = session.post(f'{server_url}/reset_password', json=RESET_PASSWORD_DATA)
        assert response.status_code == 200
        assert response.text == "Password reset successful"

        # Set the password back
        response = session.post(f'{server_url}/reset_password', json={"old_password": RESET_PASSWORD_DATA["new_password"], "new_password": VALID_CREDENTIALS["password"]})
        assert response.status_code == 200
        assert response.text == "Password reset successful"

def test_create_lecture_problem_set_problem(server_url):
    with requests.Session() as session:
        # Login
        response = session.post(f'{server_url}/login', json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.text == "Logged In"

        # Create lecture
        response = session.post(f'{server_url}/lecture/create', json=LECTURE_DATA)
        assert response.status_code == 200
        assert response.text == "Lecture Introduction to Python Created"

        # Create problem set under the created lecture
        response = session.post(f'{server_url}/l1/problemset/create', json=PROBLEM_SET_DATA)
        assert response.status_code == 200
        assert response.text == "Problem Set Problem Set 1 Created."

        # Create problem under the created problem set
        response = session.post(f'{server_url}/l1/ps1/problem/create', json=PROBLEM_DATA)
        assert response.status_code == 200
        assert response.text == "Problem created successfully"


def test_get_lecture_problem_set_problem(server_url):
    with requests.Session() as session:
        # Login
        response = session.post(f'{server_url}/login', json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.text == "Logged In"

        # Get the created lecture
        response = session.get(f'{server_url}/l1')
        assert response.status_code == 200
        lecture_data = response.json()
        assert lecture_data['title'] == "Introduction to Python"
        assert lecture_data['category'] == "technology"

        # Get list of problem sets for the lecture
        response = session.get(f'{server_url}/l1/problemsets')
        assert response.status_code == 200
        problem_sets = response.json()
        assert len(problem_sets) == 1

        # Get the created problem
        response = session.get(f'{server_url}/l1/ps1/p1')
        assert response.status_code == 200
        problem_data = response.json()
        assert problem_data['title'] == "Math Quiz"

def test_edit_lecture_problem_set_problem(server_url):
    with requests.Session() as session:
        # Login
        response = session.post(f'{server_url}/login', json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.text == "Logged In"

        # Edit the lecture
        response = session.post(f'{server_url}/l1/edit', json=UPDATED_LECTURE_DATA)
        assert response.status_code == 200
        assert "Edited" in response.text

        # Edit the problem set
        response = session.post(f'{server_url}/l1/ps1/edit', json=UPDATED_PROBLEM_SET_DATA)
        assert response.status_code == 200
        assert "Edited" in response.text

        # Edit the problem
        response = session.post(f'{server_url}/l1/ps1/p1/edit', json=UPDATED_PROBLEM_DATA)
        assert response.status_code == 200
        assert "Edited" in response.text


def test_delete_lecture_problem_set_problem(server_url):
    with requests.Session() as session:
        # Login
        response = session.post(f'{server_url}/login', json=VALID_CREDENTIALS)
        assert response.status_code == 200
        assert response.text == "Logged In"

        # Delete the lecture
        response = session.post(f'{server_url}/l1/delete')
        assert response.status_code == 200
        assert "Deleted" in response.text

        # Delete the problem set
        response = session.post(f'{server_url}/l1/ps1/delete')
        assert response.status_code == 200
        assert "Deleted" in response.text

        # Delete the problem
        response = session.post(f'{server_url}/l1/ps1/p1/delete')
        assert response.status_code == 200
        assert "Deleted" in response.text


def test_logout(server_url):
    response = requests.post(f'{server_url}/logout')
    assert response.status_code == 200
    assert response.text == "Logged Out"

if __name__ == "__main__":
    pytest.main()
