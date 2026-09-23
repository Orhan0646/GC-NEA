@app.route('/exam-question/<int:question_id>', methods=['GET', 'POST'])
def exam_question(question_id):
    if not login_required('student'):
        return redirect(url_for('student_login'))

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exam_questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    if not question:
        conn.close()
        return redirect(url_for('exam_practice'))

    if request.method == 'POST':
        response_text = request.form.get('response_text', '').strip()
        if response_text:
            cursor.execute('''
                INSERT INTO exam_responses
                    (student_id, question_id, response_text)
                VALUES (?, ?, ?)
            ''', (session['user_id'], question_id, response_text))
            conn.commit()
            conn.close()
            return redirect(url_for('exam_practice') + '?submitted=1')
        # Empty response — show error
        return render_template('exam-question.html',
            question=dict(question), error='Please write an answer.')

    # GET — check if already answered
    cursor.execute('''
        SELECT * FROM exam_responses
        WHERE student_id=? AND question_id=?
        ORDER BY date_submitted DESC LIMIT 1
    ''', (session['user_id'], question_id))
    existing = cursor.fetchone()
    conn.close()

    return render_template('exam-question.html',
        question=dict(question),
        existing=dict(existing) if existing else None,
        error=None
    )
