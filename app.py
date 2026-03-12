from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for testing
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"}
]

@app.route('/')
def home():
    return "Welcome to my Flask API!" [cite: 223]

@app.route('/student')
def get_student():
    # Get grade from query parameter, default to 0 if not provided [cite: 28]
    grade = int(request.args.get('grade', 0))
    
    # Determine pass or fail logic (75 is the passing mark) [cite: 30]
    remarks = "Pass" if grade >= 75 else "Fail"
    
    return jsonify({
        "name": "Ramnel Baynona Jr.",
        "grade": BSIT 3,
        "section": "Arduino",
        "remarks": remarks
    }) [cite: 31, 36]

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students) [cite: 94]

if __name__ == '__main__':
    app.run(debug=True) [cite: 96]