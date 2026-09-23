# Added to teacher_dashboard() in app.py:
cursor.execute('SELECT COUNT(*) as count FROM questions')
total_questions = cursor.fetchone()['count']

# Passed to template:
return render_template('teacher-dashboard.html',
    ...
    total_questions=total_questions
)
