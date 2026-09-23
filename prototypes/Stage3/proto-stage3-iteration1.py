import json

@app.route('/quiz')
def quiz():
    # Guard: student must be logged in
    if not login_required('student'):
        return redirect(url_for('student_login'))

    topic      = request.args.get('topic', 'Coastal Landscapes')
    difficulty = request.args.get('difficulty', 'medium')

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer
        FROM questions
        WHERE topic = ? AND difficulty = ?
        ORDER BY RANDOM()
        LIMIT 5
    ''', (topic, difficulty))
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # If no questions exist, redirect with error
    if not questions:
        return redirect(url_for('student_dashboard') + '?error=no_questions')

    # Serialise to JSON so JavaScript can read it directly
    questions_json = json.dumps(questions)

    return render_template('quiz.html',
        topic=topic,
        difficulty=difficulty,
        questions=questions,
        questions_json=questions_json
    )
