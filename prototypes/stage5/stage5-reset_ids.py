import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Step 1: Copy all questions into a temp table
cursor.execute("CREATE TEMP TABLE questions_backup AS SELECT * FROM questions ORDER BY id")

# Step 2: Delete all questions
cursor.execute("DELETE FROM questions")

# Step 3: Reset the autoincrement counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'questions'")

# Step 4: Re-insert questions without the old IDs (SQLite assigns fresh ones from 1)
cursor.execute("""
    INSERT INTO questions (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_answer)
    SELECT topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_answer
    FROM questions_backup
""")

conn.commit()

# Verify
cursor.execute("SELECT id, topic, question_text FROM questions ORDER BY id")
for row in cursor.fetchall():
    print(f"ID {row[0]}: [{row[1]}] {row[2][:50]}...")

conn.close()
print("\n[OK] IDs reset successfully.")