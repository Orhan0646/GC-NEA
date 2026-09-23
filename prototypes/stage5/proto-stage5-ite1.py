TOPICS       = ['Coastal Landscapes', 'River Landscapes', 'Resource Management']
DIFFICULTIES = ['easy', 'medium', 'hard']

@app.route('/manage-questions')
def manage_questions():
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    topic_filter = request.args.get('topic', '')
    diff_filter  = request.args.get('difficulty', '')

    conn   = get_connection()
    cursor = conn.cursor()

    # Build query dynamically with optional filters
    query  = 'SELECT * FROM questions WHERE 1=1'
    params = []
    if topic_filter:
        query += ' AND topic = ?'
        params.append(topic_filter)
    if diff_filter:
        query += ' AND difficulty = ?'
        params.append(diff_filter)
    query += ' ORDER BY topic, difficulty, id'

    cursor.execute(query, params)
    questions = [dict(row) for row in cursor.fetchall()]

    # Count questions per topic for stats row
    cursor.execute('SELECT topic, COUNT(*) as count FROM questions GROUP BY topic')
    topic_counts = {row['topic']: row['count'] for row in cursor.fetchall()}

    cursor.execute('SELECT COUNT(*) as count FROM questions')
    total = cursor.fetchone()['count']
    conn.close()

    return render_template('manage-questions.html',
        questions=questions, topic_counts=topic_counts, total=total,
        topics=TOPICS, difficulties=DIFFICULTIES,
        topic_filter=topic_filter, diff_filter=diff_filter
    )
