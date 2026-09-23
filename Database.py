"""
database.py - GeoChallenge Database Setup
Stage 1: Creates all tables and seeds initial data
Author: Student
"""

import sqlite3
import hashlib

# ─── Database connection ────────────────────────────────────────────
def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn


# ─── Password hashing ───────────────────────────────────────────────
def hash_password(password):
    """Hash a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


# ─── Table creation ─────────────────────────────────────────────────
def create_tables():
    """Create all database tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Students table - stores student account details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            performance_category TEXT DEFAULT 'medium'
        )
    """)

    # Teachers table - stores teacher account details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    """)

    # Questions table - stores all quiz questions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
    """)

    # Quiz results table - records every quiz attempt
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    # Progress table - tracks per-topic performance percentage
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            percentage REAL DEFAULT 0,
            category TEXT DEFAULT 'red',
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] All tables created successfully.")


# ─── Seed data ──────────────────────────────────────────────────────
def seed_data():
    """Insert demo students, teacher, and sample questions."""
    conn = get_connection()
    cursor = conn.cursor()

    # Insert demo student (only if not already present)
    cursor.execute("SELECT id FROM students WHERE username = 'student'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO students (username, password, name, class, performance_category)
            VALUES (?, ?, ?, ?, ?)
        """, ("student", hash_password("student123"), "Demo Student", "10A", "medium"))
    print("[OK] Demo student inserted.")

    cursor.execute("SELECT id FROM students WHERE username = 'student2'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO students (username, password, name, class, performance_category)
            VALUES (?, ?, ?, ?, ?)
        """, ("student2", hash_password("student456"), "Demo Student 2", "10B", "medium"))
    print("[OK] Demo student 2 inserted.")

    # Insert demo teacher
    cursor.execute("SELECT id FROM teachers WHERE username = 'teacher'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO teachers (username, password, name)
            VALUES (?, ?, ?)
        """, ("teacher", hash_password("teacher123"), "Ms. Mansell"))
    print("[OK] Demo teacher inserted.")

    # Insert sample geography questions
    questions = [
        # Coastal Landscapes - medium difficulty
        ("Coastal Landscapes", "medium",
         "What process involves waves picking up and carrying material along the coast?",
         "Hydraulic action", "Longshore drift", "Abrasion", "Attrition",
         "B"),
        ("Coastal Landscapes", "medium",
         "What landform is created when a headland arch collapses?",
         "A stack", "A spit", "A bar", "A cave",
         "A"),
        ("Coastal Landscapes", "medium",
         "Which type of wave is most destructive?",
         "Constructive wave", "Tidal wave", "Destructive wave", "Refracted wave",
         "C"),

        # River Landscapes - medium difficulty
        ("River Landscapes", "medium",
         "What is the name for the curve or bend in a river?",
         "Delta", "Meander", "Tributary", "Watershed",
         "B"),
        ("River Landscapes", "medium",
         "Which river process involves the river picking up material from its bed?",
         "Deposition", "Transportation", "Erosion", "Abrasion",
         "C"),
        ("River Landscapes", "medium",
         "What is the area of land drained by a river and its tributaries called?",
         "Flood plain", "Drainage basin", "Gorge", "Valley",
         "B"),

        # Resource Management - medium difficulty
        ("Resource Management", "medium",
         "What percentage of the Earth's water is fresh water?",
         "70%", "10%", "3%", "50%",
         "C"),
        ("Resource Management", "medium",
         "Which country is an example of a water surplus country?",
         "Egypt", "Saudi Arabia", "Brazil", "Libya",
         "C"),
        ("Resource Management", "medium",
         "What term describes the gap between food supply and demand?",
         "Food desert", "Food deficit", "Food surplus", "Food security",
         "B"),
    ]

    for q in questions:
        # Only insert if this question doesn't already exist
        cursor.execute("SELECT id FROM questions WHERE question_text = ?", (q[2],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO questions
                (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, q)

    print(f"[OK] {len(questions)} sample questions inserted.")

    # Insert starting progress records for demo student
    cursor.execute("SELECT id FROM students WHERE username = 'student'")
    student = cursor.fetchone()
    if student:
        topics = ["Coastal Landscapes", "River Landscapes", "Resource Management"]
        for topic in topics:
            cursor.execute("""
                SELECT id FROM progress WHERE student_id = ? AND topic = ?
            """, (student["id"], topic))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO progress (student_id, topic, percentage, category)
                    VALUES (?, ?, ?, ?)
                """, (student["id"], topic, 0, "red"))
        print("[OK] Starting progress records inserted.")

    conn.commit()
    conn.close()


# ─── Verification query ─────────────────────────────────────────────
def verify_database():
    """Print a summary of all data in the database to confirm setup."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- DATABASE VERIFICATION ---")

    cursor.execute("SELECT COUNT(*) as count FROM students")
    print(f"Students: {cursor.fetchone()['count']}")

    cursor.execute("SELECT COUNT(*) as count FROM teachers")
    print(f"Teachers: {cursor.fetchone()['count']}")

    cursor.execute("SELECT COUNT(*) as count FROM questions")
    print(f"Questions: {cursor.fetchone()['count']}")

    cursor.execute("SELECT COUNT(*) as count FROM progress")
    print(f"Progress records: {cursor.fetchone()['count']}")

    print("\n--- SAMPLE QUESTIONS ---")
    cursor.execute("SELECT topic, difficulty, question_text FROM questions LIMIT 3")
    for row in cursor.fetchall():
        print(f"  [{row['topic']}] ({row['difficulty']}) {row['question_text'][:60]}...")

    print("\n--- STUDENT ACCOUNTS ---")
    cursor.execute("SELECT username, name, class, performance_category FROM students")
    for row in cursor.fetchall():
        print(f"  {row['username']} | {row['name']} | {row['class']} | {row['performance_category']}")

    conn.close()
    print("\n[OK] Database verification complete.")


# ─── Run setup ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== GeoChallenge - Stage 1: Database Setup ===\n")
    create_tables()
    seed_data()
    verify_database()