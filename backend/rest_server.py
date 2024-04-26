from flask import Flask, request, jsonify
from sql_conn import get_sql_db_connection

app = Flask(__name__)

ADMIN_TOKEN = 'd4298aee-85c9-4182-ac0f-dfd1d5492163'

@app.route("/", methods=['GET'])
def root():
    return "lecture-quiz-app"

@app.route("/lecture/create", methods=['POST'])
def create_lecture():
    # authenticate token in header
    req_token = request.headers.get('token')
    if not req_token or req_token != ADMIN_TOKEN:
        return "Unauthorized", 401
    # validate input
    if not request.is_json:
        return "Invalid Input", 422
    request_json = request.get_json()
    if not request_json.get('title') or not request_json.get('body'):
        return "Invalid Input", 422
    
    # add the requested record to the database
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("INSERT INTO lectures (title, body) VALUES (%s, %s)", 
                        (request_json.get('title'), request_json.get('body')))

    return "Accepted", 200

@app.get("/lecture/<int:lecture_id>")
def get_lecture(lecture_id):
    with get_sql_db_connection() as sql_client:
        with sql_client.cursor() as cur:
            cur.execute("SELECT * FROM lectures WHERE id=%s", (lecture_id))
            query_result = cur.fetchall()
    if not query_result:
        return f'Lecture {lecture_id} not found', 404
    return jsonify(query_result), 200


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080)
    app.run(host='0.0.0.0', port=8080, debug=True) # Only enable this in development environment