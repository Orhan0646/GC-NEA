@app.route('/edit-question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    conn   = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Read updated values from form
        topic          = request.form.get('topic', '').strip()
        difficulty     = request.form.get('difficulty', '').strip()
        question_text  = request.form.get('question_text', '').strip()
        option_a       = request.form.get('option_a', '').strip()
        option_b       = request.form.get('option_b', '').strip()
        option_c       = request.form.get('option_c', '').strip()
        option_d       = request.form.get('option_d', '').strip()
        correct_answer = request.form.get('correct_answer', '').strip()

        if not all([topic, difficulty, question_text,
                    option_a, option_b, option_c, option_d, correct_answer]):
            conn.close()
            return redirect(url_for('edit_question',
                            question_id=question_id) + '?error=missing_fields')

        cursor.execute('''
            UPDATE questions
            SET topic=?, difficulty=?, question_text=?,
                option_a=?, option_b=?, option_c=?, option_d=?,
                correct_answer=?
            WHERE id=?
        ''', (topic, difficulty, question_text,
              option_a, option_b, option_c, option_d,
              correct_answer, question_id))
        conn.commit()
        conn.close()
        return redirect(url_for('manage_questions') + '?edited=1')

    # GET — fetch current values and pre-fill form
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    conn.close()

    if not question:  # Safety redirect if ID does not exist
        return redirect(url_for('manage_questions'))

    return render_template('edit-question.html',
        question=dict(question), topics=TOPICS, difficulties=DIFFICULTIES,
        error=request.args.get('error', ''))
