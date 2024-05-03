import json
from ast import literal_eval
from flask import Flask, request, jsonify, session
from flask_session import Session
from helper import sql, check_email, check_password, role_required, getproblemset_id, getproblem_id
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CATEGORIES = ["math", "technology", "chemistry", "physics", "english_language", "french_language", "history"]
USER_TYPES = ["student", "teacher", "admin"]

# -------------------------------- Home -------------------------------- #
@app.route("/", methods=["GET"])
def root():
    return "Welcome to Lecture Quiz App!", 200  # Home route

# -------------------------------- Register -------------------------------- #
@app.route("/register", methods=["POST"])
def register():
    name = request.get_json().get("name")
    username = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    type = request.get_json().get("type")

    print(email)

    usernames = sql("SELECT username FROM users")
    checkpass = check_password(password)

    if not name: return "must provide name", 403  # Check if name provided
    elif not username: return "must provide username", 403  # Check if username provided
    elif not email: return "must provide email", 403  # Check if email provided
    elif not password: return "must provide password", 403  # Check if password provided
    elif any(user_dict["username"] == username for user_dict in usernames): return "Username already taken", 403  # Check if username exists
    elif not type in USER_TYPES: return "Error: Type was not inputted / is not a valid type.", 403  # Check if type is valid
    # elif not check_email(email): return "Email is invalid", 406  # Check if email is valid
    elif not checkpass[0]: return checkpass[1], 406  # Check if password meets complexity requirements

    sql("INSERT INTO users(name, username, email, hash, type) VALUES (%s, %s, %s, %s, %s)", (name, username, email, str(generate_password_hash(password)), type))
    return "Account made succesfully.", 200  # Registration successful

# -------------------------------- Login -------------------------------- #
@app.route("/login", methods=["POST"])
def login():
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    session.clear()

    if not username: return "must provide username", 403  # Check if username provided
    elif not password: return "must provide password", 403  # Check if password provided

    print(sql("SELECT * FROM users"))
    user = sql("SELECT * FROM users WHERE username = %s", username)
    print("user", user, 1)
    user = user[0]

    if not check_password_hash(user["hash"], password):
        return "invalid username and/or password", 403  # Invalid username/password

    session["user"] = user
    session["logged_in"] = True

    return "Logged In", 200  # Login successful


# -------------------------------- Logout -------------------------------- #
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return "Logged Out", 200  # Logout successful

# -------------------------------- Update Profile -------------------------------- #
@app.route("/profile/update", methods=["POST"])
@role_required('student', 'teacher', 'admin')
def update_profile():
    user_id = session['user']['user_id']
    new_name = request.get_json().get("name")
    new_email = request.get_json().get("email")

    if not new_name and not new_email:
        return "Name or email must be provided", 422

    # Update user's name and/or email in the database
    if new_name and new_email:
        sql("UPDATE users SET name = %s, email = %s WHERE user_id = %s", (new_name, new_email, user_id))
    elif new_name:
        sql("UPDATE users SET name = %s WHERE user_id = %s", (new_name, user_id))
    else:
        sql("UPDATE users SET email = %s WHERE user_id = %s", (new_email, user_id))

    # Update session with new user information
    if new_name:
        session['user']['name'] = new_name
    if new_email:
        session['user']['email'] = new_email

    return "Profile updated successfully", 200


# -------------------------------- Reset Password -------------------------------- #
@app.route("/reset_password", methods=["POST"])
@role_required('student', 'teacher', 'admin')
def reset_password():
    user_id = session['user']['user_id']
    old_password = request.get_json().get("old_password")
    new_password = request.get_json().get("new_password")

    if not old_password or not new_password:
        return "Both old and new passwords must be provided", 422

    # Check if old password matches the current password in the database
    user = sql("SELECT * FROM users WHERE user_id = %s", user_id)
    if len(user) != 1 or not check_password_hash(user[0]["hash"], old_password):
        return "Old password is incorrect", 403

    # Check password complexity of the new password
    checkpass = check_password(new_password)
    if not checkpass[0]:
        return checkpass[1], 406

    # Update user's password hash in the database
    sql("UPDATE users SET hash = %s WHERE user_id = %s", (generate_password_hash(new_password), user_id))

    return "Password reset successful", 200


# -------------------------------- Get Lectures List -------------------------------- #
@app.route("/lectures", methods=["GET"])
def get_lectures():
    query_results = sql("SELECT lecture_id FROM lectures")
    
    if not query_results: return [], 200  # No lectures found
    return [result["lecture_id"] for result in query_results], 200  # Return lecture IDs

# -------------------------------- Create Lecture -------------------------------- #
from helper import get_sql_db_connection
@app.route("/lecture/create", methods=["POST"])
@role_required("teacher", "admin")
def create_lecture():  
    title = request.get_json().get("title").strip()
    body = request.get_json().get("body").strip()
    category = request.get_json().get("category").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    elif not title: return "Error: Title was not inputted.", 422  # Title not provided
    elif not body: return "Error: Body was not inputted.", 422  # Body not provided
    elif not category in CATEGORIES: return "Error: Category was not inputted / is not a valid category.", 422  # Invalid category
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("INSERT INTO lectures (title, body, category) VALUES (%s, %s, %s)", (title, body, category))
            lecture_id = cur.lastrowid

    return jsonify({
                "lecture_id": lecture_id,
                "message": f"Lecture {title} Created",
                    }), 200  # Lecture created

# -------------------------------- Get Lecture -------------------------------- #
@app.route("/l<int:lecture_id>", methods=["GET"])
def get_lecture(lecture_id):
    query_result = sql("SELECT * FROM lectures WHERE lecture_id=%s", lecture_id)

    if not query_result: return [], 200  # Lecture not found
    return jsonify(query_result[0]), 200  # Return lecture details

# -------------------------------- Edit Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/edit", methods=["POST"])
@role_required("teacher", "admin")
def edit_lecture(lecture_id):

    title = request.get_json().get("title").strip()
    body = request.get_json().get("body").strip()
    category = request.get_json().get("category").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    if not category in CATEGORIES: return "Error: Category was not inputted.", 422  # Invalid category
    
    sql("UPDATE lectures SET title=%s, body=%s, category=%s, modified=CURRENT_TIMESTAMP WHERE lecture_id=%s;", (title, body, category, lecture_id))

    return f"Lecture {title} Edited", 200  # Lecture edited

# -------------------------------- Delete Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/delete", methods=["POST"])
@role_required("teacher", "admin")
def delete_lecture(lecture_id):
    sql("DELETE FROM lectures WHERE lecture_id=%s;", lecture_id)

    return f"Lecture Deleted", 200  # Lecture deleted

# -------------------------------- Get Problem Sets List -------------------------------- #
@app.route("/l<int:lecture_id>/problemsets", methods=["GET"])
def get_problemsets(lecture_id):
    query_results = sql("SELECT problemset_id FROM problems WHERE lecture_id=%s", lecture_id)

    if not query_results: return [], 200  # No problem sets found
    return [result["id"] for result in query_results], 200  # Return problem set IDs

# -------------------------------- Create Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/problemset/create", methods=["POST"])
@role_required("teacher", "admin")
def create_problemset(lecture_id):

    title = request.get_json().get("title").strip()
    body = request.get_json().get("body").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    previouslectureid = sql("SELECT lecture_problemsetid FROM problemsets WHERE lecture_id=%s", lecture_id)
    if not previouslectureid:
        lecture_problemsetid = 1
    else:
        lecture_problemsetid = previouslectureid[-1]["lecture_problemsetid"] + 1

    sql("INSERT INTO problemsets (lecture_problemsetid, lecture_id, title, body) VALUES (%s, %s, %s, %s)", (lecture_problemsetid, lecture_id, title, body))

    return f"Problem Set {title} Created.", 200  # Problem set created

# -------------------------------- Get Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>", methods=["GET"])
def get_problemset(lecture_id, lecture_problemsetid):

    query_result = sql("SELECT * FROM problemsets WHERE problemset_id=%s", (getproblemset_id(lecture_id, lecture_problemsetid)))

    if not query_result: return [], 200  # Problem set not found
    return jsonify(query_result[0]), 200  # Return problem set details


# -------------------------------- Edit Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/edit", methods=["POST"])
@role_required("teacher", "admin")
def edit_problemset(lecture_id, lecture_problemsetid):
    title = request.get_json().get("title").strip()
    body = request.get_json().get("body").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("UPDATE problemsets SET title=%s, body=%s, modified=CURRENT_TIMESTAMP WHERE problemset_id=%s;", (title, body, getproblemset_id(lecture_id, lecture_problemsetid)))

    return f"Lecture {title} Edited", 200  # Lecture edited

# -------------------------------- Delete Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/delete", methods=["POST"])
@role_required("teacher", "admin")
def delete_problemset(lecture_id, lecture_problemsetid):
    sql("DELETE FROM problemsets WHERE problemset_id=%s;", getproblemset_id(lecture_id, lecture_problemsetid))

    return f"Problem Set Deleted", 200  # Problem set deleted

# -------------------------------- Get Problems List -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>", methods=["GET"])
def get_problems(lecture_id, lecture_problemsetid):
    query_results = sql("SELECT problem_id FROM problems WHERE problemset_id=%s", getproblemset_id(lecture_id, lecture_problemsetid))

    if not query_results: return [], 200  # No problems found
    return [result["id"] for result in query_results], 200  # Return problem IDs

# -------------------------------- Create Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/problem/create", methods=['POST'])
@role_required('teacher', 'admin')
def create_problem(lecture_id, lecture_problemsetid):
    if not request.get_json():
        return "Problem data must be provided", 422

    # Extract problem details from the provided data
    question = request.get_json().get("question").strip()
    option1 = request.get_json().get("option1").strip()
    option2 = request.get_json().get("option2").strip()
    option3 = request.get_json().get("option3").strip()
    option4 = request.get_json().get("option4").strip()
    correct = request.get_json().get("correct").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not question: return "Error: Body was not inputted.", 422  # Body not provided
    if not option1 or not option2 or not option3 or not option4: return "Error: Body was not inputted.", 422
    if not correct: return "Error: Body was not inputted.", 422  # Body not provided

    problemset_id = getproblemset_id(lecture_id, lecture_problemsetid)
    if not problemset_id:
        problemset_id = 1

    previous_problemset_problemid = sql("SELECT problemset_problemid FROM problems WHERE problemset_id=%s", lecture_id)
    if not previous_problemset_problemid:
        problemset_problemid = 1
    else:
        problemset_problemid = previous_problemset_problemid[-1]["problemset_problemid"] + 1


    # Insert the new problem into the database
    sql("INSERT INTO problems (problemset_id, problemset_problemid, question, option1, option2, option3, option4, correct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (problemset_id, problemset_problemid, question, option1, option2, option3, option4, correct))

    return f"Problem created successfully", 200

# -------------------------------- Get Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/p<int:problemset_problemid>", methods=["GET"])
def get_problem(lecture_id, lecture_problemsetid, problemset_problemid):
    query_result = sql("SELECT * FROM problems WHERE problem_id=%s", (getproblem_id(lecture_id, lecture_problemsetid, problemset_problemid)))

    if not query_result: return [], 200  # Problem not found
    return jsonify(query_result[0]), 200  # Return problem details

# -------------------------------- Edit Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/p<int:problemset_problemid>/edit", methods=["POST"])
@role_required("teacher", "admin")
def edit_problem(lecture_id, lecture_problemsetid, problemset_problemid):
    question = request.get_json().get("question").strip()
    option1 = request.get_json().get("option1").strip()
    option2 = request.get_json().get("option2").strip()
    option3 = request.get_json().get("option3").strip()
    option4 = request.get_json().get("option4").strip()
    correct = request.get_json().get("correct").strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not question: return "Error: Body was not inputted.", 422  # Body not provided
    if not option1 or not option2 or not option3 or not option4: return "Error: Body was not inputted.", 422
    if not correct: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("UPDATE problems SET question=%s, option1=%s, option2=%s, option3=%s, option4=%s, correct=%s, modified=CURRENT_TIMESTAMP WHERE problem_id=%s;", (question, option1, option2, option3, option4, correct, getproblem_id(lecture_id, lecture_problemsetid, problemset_problemid)))

    return f"Lecture Edited", 200  # Lecture edited

# -------------------------------- Delete Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/p<int:problemset_problemid>/delete", methods=["POST"])
@role_required("teacher", "admin")
def delete_problem(lecture_id, lecture_problemsetid, problemset_problemid):
    sql("DELETE FROM problems WHERE problem_id=%s;", getproblem_id(lecture_id, lecture_problemsetid, problemset_problemid))
    return f"Problem Deleted", 200  # Problem deleted

# -------------------------------- Check Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:lecture_problemsetid>/p<int:problemset_problemid>/check", methods=["GET"])
@role_required("teacher", "admin", "student")
def check_problem(lecture_id, lecture_problemsetid, problemset_problemid):
    answer = request.get_json().get("answer").strip()
   
    problem = sql("SELECT * FROM problems WHERE problem_id = %s", getproblem_id(lecture_id, lecture_problemsetid, problemset_problemid))[0]
    
    if answer == problem["correct"]:
        return True
    else:
        return False    

# -------------------------------- Other Code -------------------------------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)  # Run the app
