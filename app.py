
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Student Information API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00193",
        "name": "JONARD ALIPALA",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# Custom API Endpoint
@app.route('/school')
def get_school():
    return jsonify({
        "school_name": "ISUSFT",
        "location": "Philippines",
        "course": "Information Technology",
        "message": "Welcome to our school!"
    })


if __name__ == '__main__':
    app.run(debug=True)
