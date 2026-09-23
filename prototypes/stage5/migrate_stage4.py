"""
migrate_stage4.py
Run this ONCE to add the 'flagged' column to the students table.
Safe to run even if you already ran it before (uses try/except).
"""
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE students ADD COLUMN flagged INTEGER DEFAULT 0")
    conn.commit()
    print("[OK] Added 'flagged' column to students table.")
except sqlite3.OperationalError:
    print("[OK] 'flagged' column already exists. No changes needed.")

conn.close()
print("[OK] Migration complete. You can now run app.py.")