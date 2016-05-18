# all the imports
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from pymongo import MongoClient

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
client = MongoClient()
db = client.flaskr


def connect_db():
    pass


@app.route('/')
def show_entries():
    entries_coll = db.entries
    all_entries = entries_coll.find()
    entries = [dict(title=entry['title'], text=entry['text']) for entry in all_entries]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entries_coll = db.entries
    entries_coll.insert_one({"title": request.form['title'], "text": request.form['text']})
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = db.users.find({"username": username, "password": password})

        if result.count() == 0:
            error = 'Invalid user'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


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
            db.users.insert_one({"username": username, "password": password, "email": email})
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
        return render_template('register.html',
                               username='',
                               username_error=username_error,
                               email='',
                               email_error=email_error,
                               passwd_error=passwd_error,
                               confirm_pwd_error=confirm_pwd_error,
                               success=success)

    return render_template('register.html')


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(exception):
    pass


if __name__ == '__main__':
    app.run()
