
import sqlite3
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Database connection
def get_db_connection():
    db_path = os.path.join(app.root_path, 'students.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ACTIVITY 6: STUDENT INFORMATION API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00193",
        "name": "JONARD ALIPALA",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# ACTIVITY 6: GREETING API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# CUSTOM SCHOOL API
@app.route('/school')
def get_school():
    return jsonify({
        "school_name": "ISUFST",
        "location": "Philippines",
        "program": "BSIT",
        "department": "Information Technology"
    })


# ACTIVITY 7: GET ALL STUDENTS
@app.route('/students')
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ACTIVITY 7: GET ONE STUDENT BY ID
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


# ADDITIONAL API: SEARCH STUDENTS BY SECTION
@app.route('/students/section/<section>')
def get_students_by_section(section):
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section.upper(),)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == '__main__':
    app.run(debug=True, port=5001)
