from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for testing
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"}
]

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    # Get grade from query parameter, default to 0 if not provided
    # request.args.get returns a string, so we convert to int
    grade_val = request.args.get('grade', '0')
    grade = int(grade_val)
    
    # Determine pass or fail logic (75 is the passing mark)
    remarks = "Pass" if grade >= 75 else "Fail"
    
    return jsonify({
        "name": "Ramnel Baynona Jr.",
        "grade": grade,
        "section": "Arduino",
        "remarks": remarks
    })

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
