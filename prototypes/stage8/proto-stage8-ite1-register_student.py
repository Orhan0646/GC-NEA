import re  # added to imports for username validation

@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    if not login_required('teacher'):
        return redirect(url_for('teacher_login'))

    error = None
    success = None
    gen_password = None

    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip().lower()
        cls      = request.form.get('class', '').strip()

        if not all([name, username, cls]):
            error = 'All fields are required.'
        elif not re.match(r'^[a-z0-9_]+$', username):
            error = 'Username can only contain lowercase letters,
                     numbers, and underscores.'
        else:
            # Auto-generate: first name (lowercase) + '123'
            first_name   = name.split()[0].lower()
            gen_password = first_name + '123'
            hashed       = hash_password(gen_password)

            conn   = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO students
                        (username, password, name, class,
                         performance_category, flagged)
                    VALUES (?, ?, ?, ?, 'medium', 0)
                ''', (username, hashed, name, cls))
                conn.commit()
                success = f'Student {name!r} registered successfully.'
            except sqlite3.IntegrityError:
                error = f'Username {username!r} is already taken.'
                gen_password = None
            finally:
                conn.close()

    return render_template('register-student.html',
        error=error, success=success, gen_password=gen_password
    )
