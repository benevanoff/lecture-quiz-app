from flask import Flask, request, jsonify, session
from flask_session import Session
from helper import sql, check_email, check_password, role_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CATEGORIES = ['math', 'technology', 'chemistry', 'physics', 'english_language', 'french_language', 'history']
USER_TYPES = ['student', 'teacher', 'admin']

# -------------------------------- Home -------------------------------- #
@app.route("/", methods=['GET'])
def root():
    return "Welcome to Lecture Quiz App!", 200  # Home route

# -------------------------------- Register -------------------------------- #
@app.route("/register", methods=['POST'])
def register():
    name = request.get_json().get("name")
    username = request.get_json().get("username")
    email = request.get_json().get("email")
    password = request.get_json().get("password")
    type = request.get_json().get("type")

    usernames = sql("SELECT username FROM users")
    checkpass = check_password(password)

    if not name: return "must provide name", 403  # Check if name provided
    elif not username: return "must provide username", 403  # Check if username provided
    elif not email: return "must provide email", 403  # Check if email provided
    elif not password: return "must provide password", 403  # Check if password provided
    elif any(user_dict['username'] == username for user_dict in usernames): return "Username already taken", 403  # Check if username exists
    elif not type in USER_TYPES: return "Error: Type was not inputted / is not a valid type.", 403  # Check if type is valid
    elif check_email(email): return "Email is invalid", 406  # Check if email is valid
    elif checkpass[0]: return checkpass[1], 406  # Check if password meets complexity requirements

    sql("INSERT INTO users(name, username, email, hash, type) VALUES (%s, %s, %s, %s)", (name, username, email, str(generate_password_hash(password)), type))
    return "Account made succesfully.", 200  # Registration successful

# -------------------------------- Login -------------------------------- #
@app.route("/login", methods=["POST"])
def login():
    username = request.get_json().get("username")
    password = request.get_json().get("password")
    session.clear()

    if not username: return "must provide username", 403  # Check if username provided
    elif not password: return "must provide password", 403  # Check if password provided

    user = sql("SELECT * FROM users WHERE username = %s", username)

    if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
        return "invalid username and/or password", 403  # Invalid username/password

    session["user"] = user[0]
    session['logged_in'] = True

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
    ...

# -------------------------------- Reset Password -------------------------------- #
@app.route("/reset_password", methods=["POST"])
@role_required('student', 'teacher', 'admin')
def reset_password():
    ...

# -------------------------------- Get Lectures List -------------------------------- #
@app.route("/lectures", methods=['GET'])
def get_lectures():
    query_results = sql("SELECT lecture_id FROM lectures")
    
    if not query_results: return [], 200  # No lectures found
    return [result["lecture_id"] for result in query_results], 200  # Return lecture IDs

# -------------------------------- Create Lecture -------------------------------- #
@app.route("/lecture/create", methods=['POST'])
@role_required('teacher', 'admin')
def create_lecture():  
    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()
    category = request.get_json().get('category').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    elif not title: return "Error: Title was not inputted.", 422  # Title not provided
    elif not body: return "Error: Body was not inputted.", 422  # Body not provided
    elif not category in CATEGORIES: return "Error: Category was not inputted / is not a valid category.", 422  # Invalid category
    
    sql("INSERT INTO lectures (title, body, category) VALUES (%s, %s, %s)", (title, body, category))

    return f"Lecture {title} Created", 200  # Lecture created

# -------------------------------- Get Lecture -------------------------------- #
@app.route("/l<int:lecture_id>", methods=['GET'])
def get_lecture(lecture_id):
    query_result = sql("SELECT * FROM lectures WHERE lecture_id=%s", (lecture_id))

    if not query_result: return f'Lecture {lecture_id} not found', 404  # Lecture not found
    return jsonify(query_result), 200  # Return lecture details

# -------------------------------- Edit Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/edit", methods=['POST'])
@role_required('teacher', 'admin')
def edit_lecture(lecture_id):

    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()
    category = request.get_json().get('category').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    if not category in CATEGORIES: return "Error: Category was not inputted.", 422  # Invalid category
    
    sql("UPDATE lectures SET title=%s, body=%s, category=%s, modified=CURRENT_TIMESTAMP WHERE lecture_id=%s;", (title, body, category, lecture_id))

    return f"Lecture {title} Edited", 200  # Lecture edited

# -------------------------------- Delete Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/delete", methods=['POST'])
@role_required('teacher', 'admin')
def delete_lecture(lecture_id):
    req_token = request.headers.get('token')

    if session.get('logged_in') != True: return "Unauthorized", 401  # Unauthorized

    sql("DELETE FROM lectures WHERE lecture_id=%s;", lecture_id)

    return f"Lecture Deleted", 200  # Lecture deleted

# -------------------------------- Get Problem Sets List -------------------------------- #
@app.route("/l<int:lecture_id>/problemsets", methods=['GET'])
def get_problemsets(lecture_id):
    query_results = sql("SELECT problemset_id FROM problems WHERE lecture_id=%s", lecture_id)

    if not query_results: return [], 200  # No problem sets found
    return [result["id"] for result in query_results], 200  # Return problem set IDs

# -------------------------------- Create Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/problemset/create", methods=['POST'])
@role_required('teacher', 'admin')
def create_problemset(lecture_id):

    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("INSERT INTO problemsets (lecture_id, title, body) VALUES (%s, %s, %s)", (lecture_id, title, body))

    return f"Problem Set {title} Created.", 200  # Problem set created

# -------------------------------- Get Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/create", methods=['GET'])
def get_problemset(lecture_id, problemset_id):
    query_result = sql("SELECT * FROM problemsets WHERE problemset_id=%s", (problemset_id))

    if not query_result: return f'Problem Set {problemset_id} not found', 404  # Problem set not found
    return jsonify(query_result), 200  # Return problem set details

# -------------------------------- Edit Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/edit", methods=['POST'])
@role_required('teacher', 'admin')
def edit_problemset(lecture_id, problemset_id):
    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("UPDATE lectures SET title=%s, body=%s, modified=CURRENT_TIMESTAMP WHERE problemset_id=%s;", (title, body, problemset_id))

    return f"Lecture {title} Edited", 200  # Lecture edited

# -------------------------------- Delete Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/delete", methods=['POST'])
@role_required('teacher', 'admin')
def delete_problemset(lecture_id, problemset_id):
    req_token = request.headers.get('token')

    if session.get('logged_in') != True: return "Unauthorized", 401  # Unauthorized

    sql("DELETE FROM problemsets WHERE problemset_id=%s;", problemset_id)

    return f"Problem Set Deleted", 200  # Problem set deleted

# -------------------------------- Get Problems List -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>", methods=['GET'])
def get_problems(lecture_id, problemset_id):
    query_results = sql("SELECT problem_id FROM problems WHERE problemset_id=%s", problemset_id)

    if not query_results: return [], 200  # No problems found
    return [result["id"] for result in query_results], 200  # Return problem IDs

# -------------------------------- Create Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/problem/create", methods=['POST'])
@role_required('teacher', 'admin')
def create_problem(lecture_id, problemset_id):
    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("INSERT INTO problems (problemset_id, title, body) VALUES (%s, %s, %s)", (problemset_id, title, body))

    return f"Problem {title} Created.", 200  # Problem created

# -------------------------------- Get Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/problem/create", methods=['POST'])
def get_problem(lecture_id, problemset_id, problem_id):
    query_result = sql("SELECT * FROM problems WHERE problem_id=%s", (problem_id))

    if not query_result: return f'Problem {problem_id} not found', 404  # Problem not found
    return jsonify(query_result), 200  # Return problem details

# -------------------------------- Edit Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/p<int:problem_id>/edit", methods=['POST'])
@role_required('teacher', 'admin')
def edit_problem(lecture_id, problemset_id, problem_id):
    title = request.get_json().get('title').strip()
    body = request.get_json().get('body').strip()

    if not request.is_json: return "Invalid Input", 422  # Invalid input
    if not title: return "Error: Title was not inputted.", 422  # Title not provided
    if not body: return "Error: Body was not inputted.", 422  # Body not provided
    
    sql("UPDATE lectures SET title=%s, body=%s, modified=CURRENT_TIMESTAMP WHERE problem_id=%s;", (title, body, problem_id))

    return f"Lecture {title} Edited", 200  # Lecture edited

# -------------------------------- Delete Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/p<int:problem_id>/delete", methods=['POST'])
@role_required('teacher', 'admin')
def delete_problem(lecture_id, problemset_id, problem_id):
    if session.get('logged_in') != True: return "Unauthorized", 401  # Unauthorized

    sql("DELETE FROM problems WHERE problem_id=%s;", problem_id)

    return f"Problem Deleted", 200  # Problem deleted

# -------------------------------- Other Code -------------------------------- #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Run the app
