from flask import Flask, request, render_template_string, redirect, url_for, send_file
import sqlite3
import os

app = Flask(__name__)

# --- DATABASE CONNECTION SETTINGS ---
# This file will be created automatically in the same folder as app.py
DB_FILE = 'students.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  
    return conn

# Ensures the database and table are created the moment the app starts
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            section TEXT NOT NULL,
            remarks TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

BASE_STYLE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a, #2e1065); 
        min-height: 100vh; display: flex; justify-content: center; align-items: center; 
        font-family: 'Inter', system-ui, sans-serif; color: #ffffff; padding: 20px;
    }
    .card {
        background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(16px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        padding: 2.5rem; border-radius: 28px;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.7), 0 0 20px rgba(139, 92, 246, 0.1);
        text-align: center; width: 100%; max-width: 650px;
    }
    h1 { font-size: 1.8rem; margin-bottom: 1rem; color: #a5b4fc; text-shadow: 0 2px 10px rgba(165, 180, 252, 0.3); }
    .stats-bar { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 12px; margin-bottom: 20px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.1); }
    .btn {
        display: inline-block; background: linear-gradient(to right, #6366f1, #a855f7); color: white; 
        padding: 10px 18px; border-radius: 10px; text-decoration: none;
        font-weight: bold; transition: 0.3s; border: none; cursor: pointer; font-size: 0.85rem;
    }
    .btn:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4); }
    .btn-download { background: #10b981; margin-top: 10px; }
    .btn-clear { background: #334155; margin-top: 10px; }
    
    form { background: rgba(255,255,255,0.03); padding: 20px; border-radius: 18px; margin-bottom: 20px; text-align: left; border: 1px solid rgba(255,255,255,0.05); }
    .form-input { width: 100%; padding: 12px; margin: 8px 0 15px 0; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: white; }
    
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { color: #818cf8; border-bottom: 1px solid #334155; padding: 12px; text-align: left; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; }
    
    .status-badge { padding: 4px 10px; border-radius: 8px; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
    .Pass { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #22c55e; }
    .Fail { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
</style>
"""

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        students = conn.execute("SELECT * FROM students").fetchall()
        avg_res = conn.execute("SELECT AVG(grade) as average FROM students").fetchone()
        avg = avg_res['average'] if avg_res['average'] else 0
        conn.close()
    except Exception as e:
        return f"Database Error: {e}"

    rows = ""
    for s in students:
        rows += f"""
        <tr>
            <td>{s['name']}</td>
            <td>{s['grade']}</td>
            <td><span class="status-badge {s['remarks']}">{s['remarks']}</span></td>
            <td><a href="/delete/{s['id']}" style="color:#f87171; text-decoration:none; font-weight:bold;">×</a></td>
        </tr>
        """

    return render_template_string(f"""
        {BASE_STYLE}
        <div class="card">
            <h1>🚀 Student Data Console</h1>
            <div class="stats-bar">
                <b>{len(students)}</b> Records Found | Class Average: <b>{avg:.1f}%</b>
            </div>
            
            <form action="/add" method="POST">
                <input type="text" name="name" class="form-input" placeholder="Student Full Name" required>
                <input type="number" name="grade" class="form-input" placeholder="Final Grade (0-100)" required>
                <button type="submit" class="btn" style="width: 100%;">+ Register Student</button>
            </form>

            <table>
                <thead>
                    <tr><th>Name</th><th>Grade</th><th>Status</th><th></th></tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="4" style="text-align:center; opacity:0.5;">No records found.</td></tr>'}
                </tbody>
            </table>

            <div style="margin-top: 30px; display: flex; flex-direction: column; gap: 10px;">
                <a href="/students" class="btn">View API (JSON Mode)</a>
                <a href="/download" class="btn btn-download">⬇️ Download Database (.db)</a>
                <a href="/clear" class="btn btn-clear" onclick="return confirm('Delete all records?')">Reset Database</a>
            </div>
            <p style="margin-top: 25px; font-size: 0.7rem; color: #6366f1; font-weight: bold; letter-spacing: 1px;">RAMNEL BAYONA JR. | ARDUINO SECTION</p>
        </div>
    """)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    grade = int(request.form.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"
    
    conn = get_db_connection()
    conn.execute("INSERT INTO students (name, grade, section, remarks) VALUES (?, ?, ?, ?)", 
                   (name, grade, "Arduino", remarks))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/clear')
def clear_students():
    conn = get_db_connection()
    conn.execute("DELETE FROM students")
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# --- FIX: DOWNLOAD THE ACTUAL DATABASE FILE ---
@app.route('/download')
def download_db():
    if os.path.exists(DB_FILE):
        return send_file(DB_FILE, as_attachment=True)
    return "Database file not found yet. Add a student first!", 404

@app.route('/students')
def get_all():
    import json
    conn = get_db_connection()
    students = [dict(s) for s in conn.execute("SELECT * FROM students").fetchall()]
    conn.close()
    formatted_json = json.dumps(students, indent=4)
    return f"<pre>{formatted_json}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
