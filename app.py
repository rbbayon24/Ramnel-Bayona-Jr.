from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# This is our Shared CSS to keep every page looking modern and consistent
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
        text-align: center; width: 100%; max-width: 500px;
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
        font-weight: bold; margin-top: 10px; transition: 0.3s;
    }
    .btn:hover { background: #7dd3fc; transform: translateY(-2px); }
    .status-badge {
        padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
    }
    .Pass { background: #065f46; color: #34d399; }
    .Fail { background: #7f1d1d; color: #f87171; }
</style>
"""

@app.route('/')
def home():
    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <span style="font-size: 3rem;">🖥️</span>
            <h1>Student API Dashboard</h1>
            <p>Welcome, Professor! Use the buttons below to test the API logic.</p>
            <div style="display: grid; gap: 10px; margin-top: 20px;">
                <a href="/student?grade=85" class="btn">Test Pass (85)</a>
                <a href="/student?grade=60" class="btn">Test Fail (60)</a>
                <a href="/students" class="btn" style="background: #94a3b8;">View All Students</a>
            </div>
            <p style="margin-top: 20px; font-size: 0.7rem; opacity: 0.5;">Developed by Ramnel Baynona Jr.</p>
        </div>
    """)

@app.route('/student')
def get_student():
    grade = int(request.args.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"
    data = {
        "name": "Ramnel Baynona Jr.",
        "grade": grade,
        "section": "Arduino",
        "remarks": remarks
    }
    
    # Returning UI + JSON instead of just JSON
    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>Result for {data['name']}</h1>
            <div class="data-box">
                <p><strong>Grade:</strong> {data['grade']}</p>
                <p><strong>Status:</strong> <span class="status-badge {remarks}">{remarks}</span></p>
                <hr style="margin: 10px 0; opacity: 0.2;">
                <pre>{jsonify(data).get_data(as_text=True)}</pre>
            </div>
            <a href="/" class="btn">Back to Dashboard</a>
        </div>
    """)

@app.route('/students')
def get_all():
    students = [
        {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
        {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"}
    ]
    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>All Registered Students</h1>
            <div class="data-box">
                <pre>{jsonify(students).get_data(as_text=True)}</pre>
            </div>
            <a href="/" class="btn">Back to Dashboard</a>
        </div>
    """)

if __name__ == '__main__':
    app.run(debug=True)
