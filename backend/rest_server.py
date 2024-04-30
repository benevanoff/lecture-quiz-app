import pymysql
from flask import Flask, request, jsonify
from sql_conn import get_sql_db_connection

app = Flask(__name__)
CATEGORIES = ['math', 'technology', 'chemistry', 'physics', 'english_language', 'french_language', 'history']
ADMIN_TOKEN = 'd4298aee-85c9-4182-ac0f-dfd1d5492163'

# -------------------------------- Home -------------------------------- #
@app.route("/", methods=['GET'])
def root():
    return "Welcome to Lecture Quiz App!", 200

# -------------------------------- Get Lectures List -------------------------------- #
@app.route("/lectures", methods=['GET'])
def get_lectures():
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT lecture_id FROM lectures")
            query_results = cur.fetchall()
    if not query_results:
        return [], 200
    return [result["id"] for result in query_results], 200

# -------------------------------- Create Lecture -------------------------------- #
@app.route("/lecture/create", methods=['POST'])
def create_lecture():  
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()
    category = request_json.get('category').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    if not category in CATEGORIES:
        return "Error: Category was not inputted.", 422
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("INSERT INTO lectures (title, body, category) VALUES (%s, %s, %s)", (title, body, category))

    return f"Lecture {title} Created", 200

# -------------------------------- Get Lecture -------------------------------- #
@app.route("/l<int:lecture_id>", methods=['GET'])
def get_lecture(lecture_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT * FROM lectures WHERE lecture_id=%s", (lecture_id))
            query_result = cur.fetchall()
    if not query_result:
        return f'Lecture {lecture_id} not found', 404
    return jsonify(query_result), 200

# -------------------------------- Edit Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/edit", methods=['POST'])
def edit_lecture(lecture_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()
    category = request_json.get('category').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    if not category in CATEGORIES:
        return "Error: Category was not inputted.", 422
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("UPDATE lectures SET title=%s, body=%s, category=%s, modified=CURRENT_TIMESTAMP WHERE lecture_id=%s;", (title, body, category, lecture_id))

    return f"Lecture {title} Edited", 200

# -------------------------------- Delete Lecture -------------------------------- #
@app.route("/l<int:lecture_id>/delete", methods=['POST'])
def delete_lecture(lecture_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401

    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("DELETE FROM lectures WHERE lecture_id=%s;", lecture_id)

    return f"Lecture Deleted", 200

# -------------------------------- Get Problem Sets List -------------------------------- #
@app.route("/l<int:lecture_id>/problemsets", methods=['GET'])
def get_problemsets(lecture_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT problemset_id FROM problems WHERE lecture_id=%s", lecture_id)
            query_results = cur.fetchall()

    if not query_results:
        return [], 200
    return [result["id"] for result in query_results], 200

# -------------------------------- Create Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/problemset/create", methods=['POST'])
def create_problemset(lecture_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("INSERT INTO problemsets (lecture_id, title, body) VALUES (%s, %s, %s)", (lecture_id, title, body))

    return f"Problem Set {title} Created.", 200

# -------------------------------- Get Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/create", methods=['GET'])
def get_problemset(lecture_id, problemset_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT * FROM problemsets WHERE problemset_id=%s", (problemset_id))
            query_result = cur.fetchall()
    if not query_result:
        return f'Problem Set {problemset_id} not found', 404
    return jsonify(query_result), 200

# -------------------------------- Edit Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/edit", methods=['POST'])
def edit_problemset(lecture_id, problemset_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("UPDATE lectures SET title=%s, body=%s, modified=CURRENT_TIMESTAMP WHERE problemset_id=%s;", (title, body, problemset_id))

    return f"Lecture {title} Edited", 200

# -------------------------------- Delete Problem Set -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/delete", methods=['POST'])
def delete_problemset(lecture_id, problemset_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401

    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("DELETE FROM problemsets WHERE problemset_id=%s;", problemset_id)

    return f"Problem Set Deleted", 200

# -------------------------------- Get Problems List -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>", methods=['GET'])
def get_problems(lecture_id, problemset_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT problem_id FROM problems WHERE problemset_id=%s", problemset_id)
            query_results = cur.fetchall()

    if not query_results:
        return [], 200
    return [result["id"] for result in query_results], 200

# -------------------------------- Create Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/problem/create", methods=['POST'])
def create_problem(lecture_id, problemset_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("INSERT INTO problems (problemset_id, title, body) VALUES (%s, %s, %s)", (problemset_id, title, body))

    return f"Problem {title} Created.", 200

# -------------------------------- Get Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/problem/create", methods=['POST'])
def get_problem(lecture_id, problemset_id, problem_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT * FROM problems WHERE problem_id=%s", (problem_id))
            query_result = cur.fetchall()
    if not query_result:
        return f'Problem {problem_id} not found', 404
    return jsonify(query_result), 200

# -------------------------------- Edit Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/p<int:problem_id>/edit", methods=['POST'])
def edit_problem(lecture_id, problemset_id, problem_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    
    request_json = request.get_json()
    title = request_json.get('title').strip()
    body = request_json.get('body').strip()

    if not request.is_json:
        return "Invalid Input", 422
    if not title:
        return "Error: Title was not inputted.", 422
    if not body:
        return "Error: Body was not inputted.", 422
    
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("UPDATE lectures SET title=%s, body=%s, modified=CURRENT_TIMESTAMP WHERE problem_id=%s;", (title, body, category, problem_id))

    return f"Lecture {title} Edited", 200

# -------------------------------- Delete Problem -------------------------------- #
@app.route("/l<int:lecture_id>/ps<int:problemset_id>/p<int:problem_id>/delete", methods=['POST'])
def delete_problem(lecture_id, problemset_id, problem_id):
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401

    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("DELETE FROM problems WHERE problem_id=%s;", problem_id)

    return f"Problem Deleted", 200

# -------------------------------- Other Code -------------------------------- #
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=8080, debug=True) # Only enable this in development environment