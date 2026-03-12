from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# The Modern Glassmorphism UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student API | Digital Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            height: 100vh; display: flex; justify-content: center; align-items: center; 
            font-family: 'Inter', -apple-system, sans-serif; color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 3rem; border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            text-align: center; width: 100%; max-width: 450px;
        }
        .profile-img { width: 80px; height: 80px; background: #fff; border-radius: 50%; margin: 0 auto 1.5rem; display: flex; align-items: center; justify-content: center; font-size: 2rem; }
        h1 { font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.5px; }
        .section-tag { background: rgba(255, 255, 255, 0.2); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem; }
        .api-link {
            background: #fff; color: #764ba2; padding: 12px; border-radius: 12px;
            text-decoration: none; font-weight: 600; font-size: 0.9rem;
            transition: transform 0.2s, background 0.2s;
        }
        .api-link:hover { transform: translateY(-3px); background: #f0f0f0; }
        .api-link.secondary { background: transparent; color: #fff; border: 1px solid rgba(255, 255, 255, 0.4); }
        .status { margin-top: 1.5rem; font-size: 0.8rem; opacity: 0.7; }
    </style>
</head>
<body>
    <div class="container">
        <div class="profile-img">👨‍🎓</div>
        <h1>{{ name }}</h1>
        <span class="section-tag">{{ section }}</span>
        
        <p style="margin-top: 1.5rem; font-size: 0.95rem;">Interactive API Endpoints</p>
        
        <div class="grid">
            <a href="/student?grade=90" class="api-link">Check Pass</a>
            <a href="/student?grade=65" class="api-link">Check Fail</a>
            <a href="/students" class="api-link secondary">View All Data</a>
            <a href="/" class="api-link secondary">Refresh UI</a>
        </div>

        <div class="status">● System Operational | Render Cloud</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, name="Ramnel Baynona Jr.", section="Arduino")

@app.route('/student')
def get_student():
    grade_val = request.args.get('grade', '0')
    try:
        grade = int(grade_val)
    except:
        grade = 0
    remarks = "Pass" if grade >= 75 else "Fail"
    return jsonify({
        "name": "Ramnel Baynona Jr.",
        "grade": grade,
        "section": "Arduino",
        "remarks": remarks,
        "api_version": "2.0"
    })

@app.route('/students')
def get_all():
    return jsonify([
        {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
        {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"}
    ])

if __name__ == '__main__':
    app.run(debug=True)
