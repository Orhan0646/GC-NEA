def logged_in():
    """Returns True if ANY user (student or teacher) is logged in."""
    return 'user_id' in session


@app.route('/leaderboard')
def leaderboard():
    if not logged_in():
        return redirect(url_for('student_login'))

    conn   = get_connection()
    cursor = conn.cursor()

    # ── Overall ranking ──────────────────────────────────────
    # LEFT JOIN includes students with zero quiz attempts.
    # NULLS LAST puts students with no attempts at the bottom.
    cursor.execute('''
        SELECT s.id, s.name, s.performance_category,
               COUNT(qr.id) as quiz_count,
               ROUND(AVG(CAST(qr.score AS FLOAT)/qr.total_questions*100),1) as avg_pct
        FROM students s
        LEFT JOIN quiz_results qr ON qr.student_id = s.id
        GROUP BY s.id
        ORDER BY avg_pct DESC NULLS LAST, s.name ASC
    ''')
    overall = [dict(row) for row in cursor.fetchall()]

    # ── Per-topic rankings ────────────────────────────────────
    topic_data = {}
    for topic in TOPICS:
        cursor.execute('''
            SELECT s.id, s.name, s.performance_category,
                   COUNT(qr.id) as quiz_count,
                   ROUND(AVG(CAST(qr.score AS FLOAT)/qr.total_questions*100),1) as avg_pct
            FROM students s
            LEFT JOIN quiz_results qr ON qr.student_id = s.id
                                     AND qr.topic = ?
            GROUP BY s.id
            ORDER BY avg_pct DESC NULLS LAST, s.name ASC
        ''', (topic,))
        topic_data[topic] = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # Pass current_user_id only for students (None for teachers)
    current_user_id = session['user_id'] if session.get('role') == 'student' else None

    return render_template('leaderboard.html',
        overall=overall,
        topic_data=topic_data,
        topics=TOPICS,
        current_user_id=current_user_id,
        role=session.get('role')
    )
