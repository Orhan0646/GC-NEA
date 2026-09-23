import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    DELETE FROM questions
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM questions
        GROUP BY question_text
    )
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM questions")
print(f"Questions remaining: {cursor.fetchone()[0]}")

conn.close()