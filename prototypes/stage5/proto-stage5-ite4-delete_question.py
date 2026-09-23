app.route('/delete-question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if not login_required('teacher'):
        return jsonify({'error': 'Unauthorised'}), 401

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('manage_questions') + '?deleted=1')


