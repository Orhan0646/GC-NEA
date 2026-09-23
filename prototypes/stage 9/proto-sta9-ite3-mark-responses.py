@app.route('/mark-responses')
def mark_responses():
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    show = request.args.get('show', 'unmarked')

    conn   = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT er.id, er.response_text, er.marks_awarded,
               er.feedback, er.marked, er.date_submitted,
               s.name as student_name, s.class as student_class,
               eq.question_text, eq.marks as max_marks,
               eq.topic, eq.model_answer
        FROM exam_responses er
        JOIN students s        ON s.id  = er.student_id
        JOIN exam_questions eq ON eq.id = er.question_id
    '''
    if show == 'unmarked':
        query += ' WHERE er.marked = 0'
    query += ' ORDER BY er.date_submitted ASC'
    cursor.execute(query)
    responses = [dict(row) for row in cursor.fetchall()]

    cursor.execute('SELECT COUNT(*) as count FROM exam_responses WHERE marked=0')
    ungraded_count = cursor.fetchone()['count']
    conn.close()

    return render_template('mark-responses.html',
        responses=responses, show=show, ungraded_count=ungraded_count
    )


@app.route('/submit-mark/<int:response_id>', methods=['POST'])
def submit_mark(response_id):
    if not login_required('teacher'):
        return jsonify({'error': 'Unauthorised'}), 401

    marks_awarded = request.form.get('marks_awarded', '').strip()
    feedback      = request.form.get('feedback', '').strip()

    if not marks_awarded:
        return redirect(url_for('mark_responses') + '?error=no_mark')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE exam_responses
        SET marks_awarded=?, feedback=?, marked=1
        WHERE id=?
    ''', (int(marks_awarded), feedback, response_id))
    conn.commit()
    conn.close()
    return redirect(url_for('mark_responses') + '?marked=1')
