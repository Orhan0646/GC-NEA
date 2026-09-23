"""
add_test_students.py
Run ONCE to add test students for leaderboard testing.
These students have varied quiz histories so all ranking
scenarios can be properly verified.
"""
import sqlite3
import hashlib

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

conn   = sqlite3.connect('database.db')
cursor = conn.cursor()

test_students = [
    ('student2', hash_password('student123'), 'Emma Johnson',  '10A', 'top'),
    ('student3', hash_password('student123'), 'James Smith',   '10A', 'medium'),
    ('student4', hash_password('student123'), 'Aisha Patel',   '10B', 'needs_improvement'),
    ('student5', hash_password('student123'), 'Oliver Brown',  '10B', 'medium'),
    ('student6', hash_password('student123'), 'Sophie Wilson', '10A', 'top'),
]

for username, password, name, cls, band in test_students:
    try:
        cursor.execute('''
            INSERT INTO students
                (username, password, name, class, performance_category, flagged)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (username, password, name, cls, band))
        print(f'[OK] Added student: {name}')
    except sqlite3.IntegrityError:
        print(f'[SKIP] {username} already exists.')

# Add quiz results for some students — leave student6 with no attempts
# so we can test the NULLS LAST ordering on the leaderboard
cursor.execute('SELECT id FROM students WHERE username = ?', ('student2',))
s2 = cursor.fetchone()[0]
cursor.execute('SELECT id FROM students WHERE username = ?', ('student3',))
s3 = cursor.fetchone()[0]
cursor.execute('SELECT id FROM students WHERE username = ?', ('student4',))
s4 = cursor.fetchone()[0]
cursor.execute('SELECT id FROM students WHERE username = ?', ('student5',))
s5 = cursor.fetchone()[0]

quiz_results = [
    # Emma (top): high scores
    (s2, 'Coastal Landscapes', 'medium', 5, 5),
    (s2, 'River Landscapes',   'medium', 4, 5),
    (s2, 'Resource Management','medium', 5, 5),
    # James (medium): mid scores
    (s3, 'Coastal Landscapes', 'medium', 3, 5),
    (s3, 'River Landscapes',   'medium', 3, 5),
    # Aisha (needs improvement): low scores
    (s4, 'Coastal Landscapes', 'medium', 1, 5),
    (s4, 'Resource Management','medium', 2, 5),
    # Oliver (medium): mixed
    (s5, 'River Landscapes',   'medium', 4, 5),
    (s5, 'Resource Management','medium', 2, 5),
    # Sophie (top): no quiz results — tests NULLS LAST
]

for sid, topic, diff, score, total in quiz_results:
    cursor.execute('''
        INSERT INTO quiz_results
            (student_id, topic, difficulty, score, total_questions)
        VALUES (?, ?, ?, ?, ?)
    ''', (sid, topic, diff, score, total))

conn.commit()
conn.close()
print('[OK] Test students and quiz results added successfully.')
