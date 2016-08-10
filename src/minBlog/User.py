from flask import render_template, request, session, redirect, url_for
from minBlog import app, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_does_not_exist = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        exists = db.users.find({"username": username, "password": password})

        if exists.count() == 0:
            user_does_not_exist = 'User does not exist!'
        else:
            # TODO: is_logged_in / remember-me
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('show_all_entries'))

    return render_template('login.html', user_does_not_exist=user_does_not_exist)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
    return redirect(url_for('show_all_entries'))


# TODO encrypt/hash password before storing in DB
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_error = None
        email_error = None
        passwd_error = None
        confirm_pwd_error = None

        username = request.form['username']
        if username == '':
            username_error = 'Invalid username!'

        email = request.form['email']
        if email == '':
            email_error = 'Invalid e-mail!'

        password = request.form['password']
        if password == '':
            passwd_error = 'Invalid password!'

        confirm_pwd = request.form['confirm_pwd']
        if confirm_pwd == '' or confirm_pwd != password:
            confirm_pwd_error = 'Please confirm your password!'

        success = False
        if (username_error is None) and \
                (email_error is None) and \
                (passwd_error is None) and \
                (confirm_pwd_error is None):
            success = True

        if success is False:
            return render_template('register.html',
                                   username=username,
                                   username_error=username_error,
                                   email=email,
                                   email_error=email_error,
                                   passwd_error=passwd_error,
                                   confirm_pwd_error=confirm_pwd_error,
                                   success=success)

        exists = db.users.find({"username": username})
        if exists.count() != 0:
            return render_template('register.html',
                                   username=username,
                                   email=email,
                                   success=False,
                                   user_exists='User already exists!')

        db.users.insert_one({"username": username, "password": password, "email": email})
        return render_template('register.html',
                               username='',
                               username_error=username_error,
                               email='',
                               email_error=email_error,
                               passwd_error=passwd_error,
                               confirm_pwd_error=confirm_pwd_error,
                               success=success)

    return render_template('register.html')
