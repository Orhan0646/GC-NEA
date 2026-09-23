@app.route('/exam-practice')
def exam_practice():
    if not login_required('student'):
        return redirect(url_for('student_login'))

    topic_filter = request.args.get('topic', '')

    conn   = get_connection()
    cursor = conn.cursor()

    query  = 'SELECT * FROM exam_questions WHERE 1=1'
    params = []
    if topic_filter and topic_filter in TOPICS:
        query += ' AND topic = ?'
        params.append(topic_filter)
    query += ' ORDER BY topic, marks'
    cursor.execute(query, params)
    questions = [dict(row) for row in cursor.fetchall()]

    # Fetch this student's submission status for each question
    cursor.execute('''
        SELECT question_id, marked, marks_awarded
        FROM exam_responses WHERE student_id = ?
    ''', (session['user_id'],))
    answered = {row['question_id']: dict(row) for row in cursor.fetchall()}

    conn.close()
    return render_template('exam-practice.html',
        questions=questions, topics=TOPICS,
        topic_filter=topic_filter, answered=answered
    )
