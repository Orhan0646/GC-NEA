def verify_database():
    """Print a summary of all data in the database to confirm setup."""
    conn = get_connection()
    cursor = conn.cursor()

    print('--- DATABASE VERIFICATION ---')

    cursor.execute('SELECT COUNT(*) as count FROM students')
    print(f"Students: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM teachers')
    print(f"Teachers: {cursor.fetchone()['count']}")

    cursor.execute('SELECT COUNT(*) as count FROM questions')
    print(f"Questions: {cursor.fetchone()['count']}")

    cursor.execute('SELECT topic, difficulty, question_text FROM questions LIMIT 3')
    for row in cursor.fetchall():
        print(f"  [{row['topic']}] {row['question_text'][:60]}...")

    conn.close()
    print('[OK] Database verification complete.')

# Run all three functions together:
if __name__ == '__main__':
    create_tables()
    seed_data()
    verify_database()

