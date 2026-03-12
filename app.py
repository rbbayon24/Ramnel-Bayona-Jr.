from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# This is our "Temporary Database" (resets if Render sleeps, but works live!)
student_list = [
    {"name": "Ramnel Baynona Jr.", "grade": 95, "section": "Arduino", "remarks": "Pass"},
    {"name": "Juan Dela Cruz", "grade": 82, "section": "Zechariah", "remarks": "Pass"}
]

# Using your modern Shared CSS
BASE_STYLE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        min-height: 100vh; display: flex; justify-content: center; align-items: center; 
        font-family: 'Inter', system-ui, sans-serif; color: #f8fafc; padding: 20px;
    }
    .card {
        background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2.5rem; border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        text-align: center; width: 100%; max-width: 600px;
    }
    h1 { font-size: 1.5rem; margin-bottom: 1rem; color: #38bdf8; }
    .data-box { 
        background: #0f172a; padding: 15px; border-radius: 12px; 
        text-align: left; margin: 20px 0; font-family: monospace; font-size: 0.85rem;
        border-left: 4px solid #38bdf8; overflow-x: auto;
    }
    .btn {
        display: inline-block; background: #38bdf8; color: #0f172a; 
        padding: 10px 20px; border-radius: 8px; text-decoration: none;
        font-weight: bold; margin-top: 10px; transition: 0.3s; border: none; cursor: pointer;
    }
    .btn:hover { background: #7dd3fc; transform: translateY(-2px); }
    
    /* New styles for the Add Student form and Table */
    form { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px; margin-bottom: 20px; text-align: left; }
    .form-input { width: 100%; padding: 10px; margin: 5px 0 15px 0; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { color: #38bdf8; border-bottom: 1px solid #334155; padding: 10px; text-align: left; font-size: 0.8rem; }
    td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; text-align: left; }
    
    .status-badge { padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; }
    .Pass { background: #065f46; color: #34d399; }
    .Fail { background: #7f1d1d; color: #f87171; }
</style>
"""

@app.route('/')
def home():
    # Calculate Average for Summary Feature
    grades = [s['grade'] for s in student_list]
    avg = sum(grades) / len(grades) if grades else 0
    
    # Building the table rows dynamically
    rows = ""
    for s in student_list:
        rows += f"""
        <tr>
            <td>{s['name']}</td>
            <td>{s['grade']}</td>
            <td><span class="status-badge {s['remarks']}">{s['remarks']}</span></td>
        </tr>
        """

    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>🚀 Student Management API</h1>
            <p style="margin-bottom: 20px; opacity: 0.8;">Summary: <b>{len(student_list)}</b> Students | Avg: <b>{avg:.1f}</b></p>
            
            <form action="/add" method="POST">
                <label style="font-size: 0.7rem; color: #38bdf8; font-weight: bold;">NAME</label>
                <input type="text" name="name" class="form-input" placeholder="Enter student name" required>
                <label style="font-size: 0.7rem; color: #38bdf8; font-weight: bold;">GRADE</label>
                <input type="number" name="grade" class="form-input" placeholder="Enter grade (0-100)" required>
                <button type="submit" class="btn" style="width: 100%;">Add Student to API</button>
            </form>

            <table>
                <thead>
                    <tr><th>STUDENT</th><th>GRADE</th><th>STATUS</th></tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>

            <div style="margin-top: 20px;">
                <a href="/students" class="btn" style="background: #94a3b8;">View Raw JSON Data</a>
            </div>
            <p style="margin-top: 20px; font-size: 0.6rem; opacity: 0.4;">Developed by Ramnel Baynona Jr.</p>
        </div>
    """)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    grade = int(request.form.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"
    
    student_list.append({
        "name": name, 
        "grade": grade, 
        "section": "Arduino", 
        "remarks": remarks
    })
    return home() # Reload home with the new data

@app.route('/student')
def get_student():
    grade = int(request.args.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"
    data = {"name": "Search Result", "grade": grade, "section": "Arduino", "remarks": remarks}
    
    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>API Logic Analysis</h1>
            <div class="data-box">
                <p><strong>Grade:</strong> {grade}</p>
                <p><strong>Status:</strong> <span class="status-badge {remarks}">{remarks}</span></p>
                <hr style="margin: 10px 0; opacity: 0.2;">
                <pre>{jsonify(data).get_data(as_text=True)}</pre>
            </div>
            <a href="/" class="btn">Back to Dashboard</a>
        </div>
    """)

@app.route('/students')
def get_all():
    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>All Students JSON</h1>
            <div class="data-box">
                <pre>{jsonify(student_list).get_data(as_text=True)}</pre>
            </div>
            <a href="/" class="btn">Back to Dashboard</a>
        </div>
    """)

if __name__ == '__main__':
    app.run(debug=True)
