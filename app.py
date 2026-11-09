
import sqlite3
import os
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    db_path = os.path.join(app.root_path, 'students.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ACTIVITY 6: STUDENT INFORMATION
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00193",
        "name": "JONARD ALIPAL",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# ACTIVITY 6: GREETING
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({"message": f"Hello, {name}!"})


# ACTIVITY 6: CUSTOM SCHOOL API
@app.route('/school')
def get_school():
    return jsonify({
        "school_name": "Your School Name",
        "location": "Philippines",
        "program": "BSIT",
        "department": "Information Technology"
    })


# ACTIVITY 7: GET ALL STUDENTS
@app.route('/students')
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students ORDER BY id'
    ).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


# ACTIVITY 7: GET ONE STUDENT
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ACTIVITY 7: SEARCH BY SECTION
@app.route('/students/section/<section>')
def get_students_by_section(section):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section.upper(),)
    ).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


# ACTIVITY 8: CREATE STUDENT
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required = ['student_id', 'name', 'program', 'year', 'section']

    if any(not str(data.get(field, '')).strip() for field in required):
        return jsonify({"error": "All fields are required"}), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Year must be a positive number"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        '''INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)''',
        (
            data['student_id'].strip(),
            data['name'].strip(),
            data['program'].strip(),
            year,
            data['section'].strip().upper()
        )
    )

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student added successfully",
        "id": new_id
    }), 201


# ACTIVITY 8: READ ONE STUDENT
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ACTIVITY 8: UPDATE STUDENT
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    required = ['student_id', 'name', 'program', 'year', 'section']

    if any(not str(data.get(field, '')).strip() for field in required):
        return jsonify({"error": "All fields are required"}), 400

    try:
        year = int(data['year'])
        if year < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid year"}), 400

    conn = get_db_connection()

    existing = conn.execute(
        'SELECT id FROM students WHERE id = ?', (id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute(
        '''UPDATE students
        SET student_id=?, name=?, program=?, year=?, section=?
        WHERE id=?''',
        (
            data['student_id'].strip(),
            data['name'].strip(),
            data['program'].strip(),
            year,
            data['section'].strip().upper(),
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated successfully"})


# ACTIVITY 8: DELETE STUDENT
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    cursor = conn.execute(
        'DELETE FROM students WHERE id = ?', (id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"})


# CLASSMATE API PLACEHOLDER
# Replace this URL when your classmate gives it to you.
CLASSMATE_API = "https://myranie-arch.onrender.com/"


# RETRIEVE CLASSMATE RECORDS (READ ONLY)
@app.route('/api/classmate/students')
def get_classmate_students():
    if not CLASSMATE_API.startswith('https://'):
        return jsonify({
            "error": "Classmate API URL has not been configured yet."
        }), 400

    try:
        with urlopen(CLASSMATE_API, timeout=20) as response:
            if response.status != 200:
                return jsonify({"error": "Classmate API request failed"}), 502

            data = json.loads(response.read().decode('utf-8'))

            if not isinstance(data, list):
                return jsonify({"error": "Invalid classmate API response"}), 502

            return jsonify(data)

    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        return jsonify({
            "error": "Unable to retrieve classmate records.",
            "details": str(error)
        }), 502


if __name__ == '__main__':
    app.run(debug=True, port=5001)
