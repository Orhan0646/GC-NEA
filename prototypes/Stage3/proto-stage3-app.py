"""
app.py - GeoChallenge Flask Backend
Stage 2: User Authentication, Sessions, and Routing
Author: Student
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
import json

# ─── App setup ──────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "geochallenge_secret_2024"  # Required for session encryption


# ─── Helper functions ────────────────────────────────────────────────
def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    """Hash a password using SHA-256 before comparing to database."""
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(role):
    """Check if a user is logged in with the correct role."""
    return "user_id" in session and session.get("role") == role


# ─── Home route ─────────────────────────────────────────────────────
@app.route("/")
def home():
    """Serve the homepage."""
    return render_template("index.html")


# ─── Student login ───────────────────────────────────────────────────
@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    """
    GET:  Show the student login page.
    POST: Validate credentials against the database.
          On success: store user in session, redirect to dashboard.
          On failure: return login page with error message.
    """
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Validate: fields must not be empty
        if not username or not password:
            error = "Please enter both username and password."
        else:
            # Query the database for the student
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE username = ?", (username,)
            )
            student = cursor.fetchone()
            conn.close()

            # Check if student exists and password matches
            if student and student["password"] == hash_password(password):
                # Store user details in session
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
    """
    GET:  Show the teacher login page.
    POST: Validate teacher credentials against the database.
    """
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            error = "Please enter both username and password."
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM teachers WHERE username = ?", (username,)
            )
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
    """Show student dashboard - requires student to be logged in."""
    if not login_required("student"):
        return redirect(url_for("student_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch this student's progress for all 3 topics
    cursor.execute(
        "SELECT topic, percentage, category FROM progress WHERE student_id = ?",
        (session["user_id"],)
    )
    progress_rows = cursor.fetchall()
    conn.close()

    # Convert to a dict for easy template access: { "Coastal Landscapes": {...}, ... }
    progress = {row["topic"]: dict(row) for row in progress_rows}

    return render_template(
        "student-dashboard.html",
        name=session["name"],
        performance_category=session["performance_category"],
        progress=progress
    )


# ─── Teacher dashboard ───────────────────────────────────────────────
@app.route("/teacher-dashboard")
def teacher_dashboard():
    """Show teacher dashboard - requires teacher to be logged in."""
    if not login_required("teacher"):
        return redirect(url_for("teacher_login"))

    conn = get_connection()
    cursor = conn.cursor()

    # Count total students
    cursor.execute("SELECT COUNT(*) as count FROM students")
    total_students = cursor.fetchone()["count"]

    # Count students by performance category
    cursor.execute(
        "SELECT performance_category, COUNT(*) as count FROM students GROUP BY performance_category"
    )
    category_counts = {row["performance_category"]: row["count"] for row in cursor.fetchall()}

    # Average score per topic across all quiz results
    cursor.execute("""
        SELECT topic,
               ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as avg_pct
        FROM quiz_results
        GROUP BY topic
    """)
    topic_averages = {row["topic"]: row["avg_pct"] for row in cursor.fetchall()}

    conn.close()

    return render_template(
        "teacher-dashboard.html",
        name=session["name"],
        total_students=total_students,
        category_counts=category_counts,
        topic_averages=topic_averages
    )


# ─── Quiz ────────────────────────────────────────────────────────────
@app.route("/quiz")
def quiz():
    """
    Load the quiz page for a given topic and difficulty.
    Fetches questions from the database and passes them to the template.
    Query params: ?topic=Coastal+Landscapes&difficulty=medium
    """
    if not login_required("student"):
        return redirect(url_for("student_login"))

    topic      = request.args.get("topic", "Coastal Landscapes")
    difficulty = request.args.get("difficulty", "medium")

    conn   = get_connection()
    cursor = conn.cursor()
    # Fetch up to 5 questions for this topic and difficulty, randomised
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
        # If no questions found, redirect dashboard with a flash-style param
        return redirect(url_for("student_dashboard") + "?error=no_questions")

    # Serialise questions to JSON so JavaScript can use them directly
    questions_json = json.dumps(questions)

    return render_template(
        "quiz.html",
        topic=topic,
        difficulty=difficulty,
        questions=questions,
        questions_json=questions_json
    )


# ─── Submit quiz results ──────────────────────────────────────────────
@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    """
    Receives quiz results from JavaScript (fetch POST).
    Saves score to quiz_results table.
    Recalculates progress percentage and updates the progress table.
    Returns JSON with new performance band if it changed.
    """
    if not login_required("student"):
        return jsonify({"error": "Not logged in"}), 401

    data            = request.get_json()
    topic           = data.get("topic")
    difficulty      = data.get("difficulty")
    score           = int(data.get("score", 0))
    total_questions = int(data.get("total_questions", 1))

    student_id      = session["user_id"]
    percentage      = round((score / total_questions) * 100, 1)

    conn   = get_connection()
    cursor = conn.cursor()

    # 1. Save this quiz attempt
    cursor.execute("""
        INSERT INTO quiz_results (student_id, topic, difficulty, score, total_questions)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, topic, difficulty, score, total_questions))

    # 2. Recalculate average score for this topic across all attempts
    cursor.execute("""
        SELECT ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as avg_pct
        FROM quiz_results
        WHERE student_id = ? AND topic = ?
    """, (student_id, topic))
    avg_pct = cursor.fetchone()["avg_pct"] or percentage

    # 3. Determine colour category from average percentage
    if avg_pct >= 70:
        category = "green"
    elif avg_pct >= 40:
        category = "amber"
    else:
        category = "red"

    # 4. Update (or insert) the progress row for this topic
    cursor.execute("""
        SELECT id FROM progress WHERE student_id = ? AND topic = ?
    """, (student_id, topic))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE progress SET percentage = ?, category = ?
            WHERE student_id = ? AND topic = ?
        """, (avg_pct, category, student_id, topic))
    else:
        cursor.execute("""
            INSERT INTO progress (student_id, topic, percentage, category)
            VALUES (?, ?, ?, ?)
        """, (student_id, topic, avg_pct, category))

    # 5. Recalculate overall performance band from all topics combined
    cursor.execute("""
        SELECT ROUND(AVG(CAST(score AS FLOAT) / total_questions * 100), 1) as overall
        FROM quiz_results WHERE student_id = ?
    """, (student_id,))
    overall = cursor.fetchone()["overall"] or 0

    if overall >= 70:
        new_category = "top"
    elif overall >= 40:
        new_category = "medium"
    else:
        new_category = "needs_improvement"

    # 6. Update student's overall performance category
    old_category = session.get("performance_category")
    cursor.execute("""
        UPDATE students SET performance_category = ? WHERE id = ?
    """, (new_category, student_id))
    session["performance_category"] = new_category

    conn.commit()
    conn.close()

    # Return new_category only if it changed (JavaScript shows a notification)
    response = {"status": "saved", "percentage": avg_pct, "category": category}
    if new_category != old_category:
        response["new_category"] = new_category

    return jsonify(response)


# ─── Logout ──────────────────────────────────────────────────────────
@app.route("/logout")
def logout():
    """Clear the session and redirect to home."""
    session.clear()
    return redirect(url_for("home"))


# ─── Run the app ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)