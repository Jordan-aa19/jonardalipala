from flask import Flask, jsonify, request

app = Flask(__name__)

# Home Endpoint
@app.route('/')
def home():
    return "Welcome to Jorand Alipala's Flask API!"

# Student Endpoint
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00193",
        "name": "Jonard Alipala",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })

# Hello Endpoint
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

# NEW ENDPOINT 1: About Me
@app.route('/about')
def about():
    return jsonify({
        "name": "Jonard Alipala",
        "program": "BSIT",
        "year": 3,
        "section": "A",
        "interest": "Electrical Engineering"
    })

# NEW ENDPOINT 2: Greeting with Input
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Friend')
    return jsonify({
        "message": f"Hello {name}! Welcome to Alipala's API.",
        "creator": "Jonard Alipala"
    })

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)