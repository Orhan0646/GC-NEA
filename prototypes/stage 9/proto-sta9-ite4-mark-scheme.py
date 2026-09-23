@app.route('/mark-scheme')
def mark_scheme():
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    topic_filter = request.args.get('topic', '')
    marks_filter = request.args.get('marks', '')

    conn   = get_connection()
    cursor = conn.cursor()

    query  = 'SELECT * FROM exam_questions WHERE 1=1'
    params = []
    if topic_filter and topic_filter in TOPICS:
        query += ' AND topic = ?'
        params.append(topic_filter)
    if marks_filter and marks_filter.isdigit():
        query += ' AND marks = ?'
        params.append(int(marks_filter))
    query += ' ORDER BY topic, marks, id'
    cursor.execute(query, params)
    questions = [dict(row) for row in cursor.fetchall()]

    cursor.execute('SELECT topic, COUNT(*) as count FROM exam_questions GROUP BY topic')
    topic_counts = {row['topic']: row['count'] for row in cursor.fetchall()}
    cursor.execute('SELECT COUNT(*) as count FROM exam_questions')
    total = cursor.fetchone()['count']
    cursor.execute('SELECT DISTINCT marks FROM exam_questions ORDER BY marks')
    mark_values = [row['marks'] for row in cursor.fetchall()]

    conn.close()
    return render_template('mark-scheme.html',
        questions=questions, topics=TOPICS,
        topic_counts=topic_counts, total=total,
        mark_values=mark_values,
        topic_filter=topic_filter, marks_filter=marks_filter
    )
