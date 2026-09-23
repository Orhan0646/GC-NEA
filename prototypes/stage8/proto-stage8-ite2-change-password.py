@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if not login_required('student'):
        return redirect(url_for('student_login'))

    error   = None
    success = None

    if request.method == 'POST':
        current_pw = request.form.get('current_password', '')
        new_pw     = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_password', '')

        if not all([current_pw, new_pw, confirm_pw]):
            error = 'All fields are required.'
        elif new_pw != confirm_pw:
            error = 'New password and confirmation do not match.'
        elif len(new_pw) < 6:
            error = 'New password must be at least 6 characters.'
        else:
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password FROM students WHERE id = ?',
                (session['user_id'],)
            )
            row = cursor.fetchone()

            if row['password'] != hash_password(current_pw):
                error = 'Current password is incorrect.'
                conn.close()
            else:
                cursor.execute(
                    'UPDATE students SET password = ? WHERE id = ?',
                    (hash_password(new_pw), session['user_id'])
                )
                conn.commit()
                conn.close()
                success = 'Your password has been changed successfully.'

    return render_template('change-password.html',
        error=error, success=success
    )
