"""
app.py - GeoChallenge Flask Backend
Stage 4: Live Teacher Dashboard, Student History, Flag for Support
Author: Student
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
import json

# ─── App setup ──────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "geochallenge_secret_2024"


# ─── Helper functions ────────────────────────────────────────────────
def get_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(role):
    return "user_id" in session and session.get("role") == role


# ─── Home ────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


# ─── Student login ───────────────────────────────────────────────────
@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Please enter both username and password."
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE username = ?", (username,))
            student = cursor.fetchone()
            conn.close()
            if student and student["password"] == hash_password(password):
                session["user_id"] = student["id"]
                session["username"] = student["username"]
                session["name"] = student["name"]
                session["role"] = "student"
                session["performance_category"] = student["performance_category"]
                return redirect(url_for("student_dashboard"))
            else:
                error = "Invalid username or password. Please try again."
    return render_template("student-login.html", error=error)


# ─── Teacher login ───────────────────────────────────────────────────
@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Please enter both username and password."
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
            teacher = cursor.fetchone()
            conn.close()
            if teacher and teacher["password"] == hash_password(password):
                session["user_id"] = teacher["id"]
                session["username"] = teacher["username"]
                session["name"] = teacher["name"]
                session["role"] = "teacher"
                return redirect(url_for("teacher_dashboard"))
            else:
                error = "Invalid username or password. Please try again."
    return render_template("teacher-login.html", error=error)


# ─── Student dashboard ───────────────────────────────────────────────
@app.route("/student-dashboard")
def student_dashboard():
    if not login_required("student"):
        return redirect(url_for("student_login"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT topic, percentage, category FROM progress WHERE student_id = ?",
        (session["user_id"],)
    )
    progress_rows = cursor.fetchall()
    conn.close()
    progress = {row["topic"]: dict(row) for row in progress_rows}
    return render_template(
        "student-dashboard.html",
        name=session["name"],
        performance_category=session["performance_category"],
        progress=progress
    )


# ─── Teacher dashboard (Stage 4 — fully live) ────────────────────────
@app.route("/teacher-dashboard")
def teacher_dashboard():
    if not login_required("teacher"):
        return redirect(url_for("teacher_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # ── 1. Total student count ────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) as count FROM students")
    total_students = cursor.fetchone()["count"]

    # ── 2. Students per performance band ─────────────────────────────
    cursor.execute("""
        SELECT performance_category, COUNT(*) as count
        FROM students
        GROUP BY performance_category
    """)
    category_counts = {row["performance_category"]: row["count"] for row in cursor.fetchall()}

    # ── 3. Class average per topic (from all quiz results) ───────────
    cursor.execute("""
        SELECT topic,
               ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as avg_pct
        FROM quiz_results
        GROUP BY topic
    """)
    topic_averages = {row["topic"]: row["avg_pct"] for row in cursor.fetchall()}

    # ── 4. Full student list with per-topic scores ────────────────────
    cursor.execute("""
        SELECT s.id, s.name, s.class, s.performance_category, s.flagged,
               p1.percentage as coastal_pct,   p1.category as coastal_cat,
               p2.percentage as river_pct,     p2.category as river_cat,
               p3.percentage as resource_pct,  p3.category as resource_cat
        FROM students s
        LEFT JOIN progress p1 ON p1.student_id = s.id AND p1.topic = 'Coastal Landscapes'
        LEFT JOIN progress p2 ON p2.student_id = s.id AND p2.topic = 'River Landscapes'
        LEFT JOIN progress p3 ON p3.student_id = s.id AND p3.topic = 'Resource Management'
        ORDER BY s.name
    """)
    students = [dict(row) for row in cursor.fetchall()]

    # ── 5. Total quiz attempts across all students ────────────────────
    cursor.execute("SELECT COUNT(*) as count FROM quiz_results")
    total_attempts = cursor.fetchone()["count"]

    conn.close()

    return render_template(
        "teacher-dashboard.html",
        name=session["name"],
        total_students=total_students,
        total_attempts=total_attempts,
        category_counts=category_counts,
        topic_averages=topic_averages,
        students=students
    )


# ─── Student history (Stage 4 — new route) ───────────────────────────
@app.route("/student-history/<int:student_id>")
def student_history(student_id):
    """Show a specific student's full quiz history. Teacher only."""
    if not login_required("teacher"):
        return redirect(url_for("teacher_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Student details
    cursor.execute("SELECT id, name, class, performance_category, flagged FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return redirect(url_for("teacher_dashboard"))

    # All quiz attempts for this student, most recent first
    cursor.execute("""
        SELECT topic, difficulty, score, total_questions,
               ROUND(CAST(score AS FLOAT) / total_questions * 100, 1) as percentage,
               date_taken
        FROM quiz_results
        WHERE student_id = ?
        ORDER BY date_taken DESC
    """, (student_id,))
    attempts = [dict(row) for row in cursor.fetchall()]

    # Progress per topic
    cursor.execute("""
        SELECT topic, percentage, category
        FROM progress
        WHERE student_id = ?
    """, (student_id,))
    progress = {row["topic"]: dict(row) for row in cursor.fetchall()}

    conn.close()

    return render_template(
        "student-history.html",
        student=dict(student),
        attempts=attempts,
        progress=progress
    )


# ─── Flag / unflag student (Stage 4 — new route) ─────────────────────
@app.route("/flag-student/<int:student_id>", methods=["POST"])
def flag_student(student_id):
    """Toggle the flagged status of a student. Teacher only. Returns JSON."""
    if not login_required("teacher"):
        return jsonify({"error": "Unauthorised"}), 401

    conn = get_connection()
    cursor = conn.cursor()

    # Get current flag status and toggle it
    cursor.execute("SELECT flagged FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    new_flag = 0 if row["flagged"] else 1
    cursor.execute("UPDATE students SET flagged = ? WHERE id = ?", (new_flag, student_id))
    conn.commit()
    conn.close()

    return jsonify({"flagged": bool(new_flag)})


# ─── Quiz ────────────────────────────────────────────────────────────
@app.route("/quiz")
def quiz():
    if not login_required("student"):
        return redirect(url_for("student_login"))
    topic      = request.args.get("topic", "Coastal Landscapes")
    difficulty = request.args.get("difficulty", "medium")
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer
        FROM questions
        WHERE topic = ? AND difficulty = ?
        ORDER BY RANDOM()
        LIMIT 5
    """, (topic, difficulty))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    if not questions:
        return redirect(url_for("student_dashboard") + "?error=no_questions")
    return render_template(
        "quiz.html",
        topic=topic,
        difficulty=difficulty,
        questions=questions,
        questions_json=json.dumps(questions)
    )


# ─── Submit quiz ─────────────────────────────────────────────────────
@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    if not login_required("student"):
        return jsonify({"error": "Not logged in"}), 401
    data            = request.get_json()
    topic           = data.get("topic")
    difficulty      = data.get("difficulty")
    score           = int(data.get("score", 0))
    total_questions = int(data.get("total_questions", 1))
    student_id      = session["user_id"]
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_results (student_id, topic, difficulty, score, total_questions)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, topic, difficulty, score, total_questions))
    cursor.execute("""
        SELECT ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as avg_pct
        FROM quiz_results WHERE student_id = ? AND topic = ?
    """, (student_id, topic))
    avg_pct  = cursor.fetchone()["avg_pct"] or 0
    category = "green" if avg_pct >= 70 else "amber" if avg_pct >= 40 else "red"
    cursor.execute("SELECT id FROM progress WHERE student_id = ? AND topic = ?", (student_id, topic))
    if cursor.fetchone():
        cursor.execute("UPDATE progress SET percentage = ?, category = ? WHERE student_id = ? AND topic = ?",
                       (avg_pct, category, student_id, topic))
    else:
        cursor.execute("INSERT INTO progress (student_id, topic, percentage, category) VALUES (?, ?, ?, ?)",
                       (student_id, topic, avg_pct, category))
    cursor.execute("""
        SELECT ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as overall
        FROM quiz_results WHERE student_id = ?
    """, (student_id,))
    overall      = cursor.fetchone()["overall"] or 0
    new_category = "top" if overall >= 70 else "medium" if overall >= 40 else "needs_improvement"
    old_category = session.get("performance_category")
    cursor.execute("UPDATE students SET performance_category = ? WHERE id = ?", (new_category, student_id))
    session["performance_category"] = new_category
    conn.commit()
    conn.close()
    response = {"status": "saved", "percentage": avg_pct, "category": category}
    if new_category != old_category:
        response["new_category"] = new_category
    return jsonify(response)


# ─── Logout ──────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ─── Run ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)