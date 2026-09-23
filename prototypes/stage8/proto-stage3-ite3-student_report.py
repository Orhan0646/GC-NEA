@app.route('/student-report/<int:student_id>')
def student_report(student_id):
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, name, class, performance_category FROM students WHERE id = ?',
        (student_id,)
    )
    student = cursor.fetchone()
    if not student:
        conn.close()
        return redirect(url_for('teacher_dashboard'))

    cursor.execute('''
        SELECT topic, difficulty, score, total_questions,
               ROUND(CAST(score AS FLOAT)/total_questions*100,1) as percentage,
               date_taken
        FROM quiz_results
        WHERE student_id = ?
        ORDER BY date_taken DESC
    ''', (student_id,))
    attempts = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        'SELECT topic, percentage, category FROM progress WHERE student_id = ?',
        (student_id,)
    )
    progress = {row['topic']: dict(row) for row in cursor.fetchall()}

    # Calculate summary statistics in Python
    total_attempts = len(attempts)
    overall_avg    = round(
        sum(a['percentage'] for a in attempts) / total_attempts, 1
    ) if total_attempts > 0 else 0

    conn.close()
    return render_template('student-report.html',
        student=dict(student), attempts=attempts,
        progress=progress, total_attempts=total_attempts,
        overall_avg=overall_avg
    )
