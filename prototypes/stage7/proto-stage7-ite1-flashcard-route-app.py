@app.route('/flashcards')
def flashcards():
    if not login_required('student'):
        return redirect(url_for('student_login'))

    topic      = request.args.get('topic', '')
    difficulty = request.args.get('difficulty', '')

    # No selection yet — render picker screen only
    if not topic or not difficulty:
        return render_template('flashcards.html',
            topics=TOPICS, difficulties=DIFFICULTIES,
            cards=None, topic=topic, difficulty=difficulty, card_count=0
        )

    # Validate inputs against allowed values
    if topic not in TOPICS or difficulty not in DIFFICULTIES:
        return redirect(url_for('flashcards'))

    conn   = get_connection()
    cursor = conn.cursor()

    # Fetch all questions for this topic/difficulty, randomised
    cursor.execute('''
        SELECT question_text, option_a, option_b, option_c, option_d, correct_answer
        FROM questions
        WHERE topic = ? AND difficulty = ?
        ORDER BY RANDOM()
    ''', (topic, difficulty))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return render_template('flashcards.html',
            topics=TOPICS, difficulties=DIFFICULTIES,
            cards=None, topic=topic, difficulty=difficulty,
            card_count=0, no_cards=True
        )

    # Build card list — resolve correct letter to full answer text
    cards = []
    for row in rows:
        letter     = row['correct_answer']
        option_map = {
            'A': row['option_a'], 'B': row['option_b'],
            'C': row['option_c'], 'D': row['option_d'],
        }
        cards.append({
            'question':       row['question_text'],
            'correct_letter': letter,
            'correct_text':   option_map[letter],
            'option_a':       row['option_a'],
            'option_b':       row['option_b'],
            'option_c':       row['option_c'],
            'option_d':       row['option_d'],
        })

    return render_template('flashcards.html',
        topics=TOPICS, difficulties=DIFFICULTIES,
        cards=cards, cards_json=json.dumps(cards),
        topic=topic, difficulty=difficulty,
        card_count=len(cards), no_cards=False
    )
