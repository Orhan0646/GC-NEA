@app.route('/add-question', methods=['POST'])
def add_question():
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    # Read all form fields
    topic          = request.form.get('topic', '').strip()
    difficulty     = request.form.get('difficulty', '').strip()
    question_text  = request.form.get('question_text', '').strip()
    option_a       = request.form.get('option_a', '').strip()
    option_b       = request.form.get('option_b', '').strip()
    option_c       = request.form.get('option_c', '').strip()
    option_d       = request.form.get('option_d', '').strip()
    correct_answer = request.form.get('correct_answer', '').strip()

    # Server-side validation: all 8 fields must be filled
    if not all([topic, difficulty, question_text, option_a,
                option_b, option_c, option_d, correct_answer]):
        return redirect(url_for('manage_questions') + '?error=missing_fields')

    # Validate topic and difficulty are allowed values
    if topic not in TOPICS or difficulty not in DIFFICULTIES:
        return redirect(url_for('manage_questions') + '?error=invalid_values')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions
            (topic, difficulty, question_text,
             option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (topic, difficulty, question_text,
          option_a, option_b, option_c, option_d, correct_answer))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_questions') + '?success=1')
