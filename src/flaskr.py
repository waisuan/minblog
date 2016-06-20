# all the imports
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from pymongo import MongoClient
from bson import ObjectId
import time
import re
import Paginator
import os

# configuration
DEBUG = True
SECRET_KEY = '\xf6\x82R\xbeK\xa1QD\x03\xaa\x9a-\xd9\x1d\xc0$7XK\x0eo6\x1d\x05'
# development key
# \xf6\x82R\xbeK\xa1QD\x03\xaa\x9a-\xd9\x1d\xc0$7XK\x0eo6\x1d\x05
# USERNAME = 'admin'
# PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
# app.secret_key = os.urandom(24)
client = MongoClient()
db = client.flaskr
paginator = Paginator.Paginator(3)


def connect_db():
    pass


@app.route('/')
@app.route('/<navigate>')
def show_entries(navigate=None):
    curr_user = session['username']
    if navigate == 'next':
        all_entries = paginator.page_next(curr_user)
    elif navigate == 'prev':
        all_entries = paginator.page_prev(curr_user)
    else:
        entries_coll = db.entries
        all_entries = entries_coll.find({"username": curr_user})
        paginator.insert(curr_user, all_entries)
        all_entries = paginator.page_next(curr_user)
    # print all_entries
    has_more_pages = paginator.has_more_pages(curr_user)
    has_prev_pages = paginator.has_prev_pages(curr_user)
    entries = [dict(id=entry['_id'],
                    author=entry['username'],
                    date=entry['date'],
                    time=entry['time'],
                    title=entry['title'],
                    text=entry['text'],
                    modified=entry['modified']) for entry in all_entries]
    return render_template('show_entries.html', entries=entries,
                           has_more_pages=has_more_pages,
                           has_prev_pages=has_prev_pages)


@app.route('/new', methods=['GET', 'POST'])
def add_entry():
    # if not session.get('logged_in'):
    #    abort(401)
    # entries_coll = db.entries
    # entries_coll.insert_one({"title": request.form['title'], "text": request.form['text']})
    # flash('New entry was successfully posted')
    # return redirect(url_for('show_entries'))
    if request.method == 'POST':
        entry_text = request.form['entry_text']
        entry_text = filter_entry_text(entry_text)
        # regexp = re.compile(r'<div>')
        # if regexp.search(request.form['entry_text']) is not None:
        #    entry_text = '<div>' + re.sub('<div>', '</div><div>', request.form['entry_text'], 1)
        now_date = time.strftime("%d/%m/%Y")
        now_time = time.strftime("%I:%M %p")
        db.entries.insert_one({"username": session['username'],
                               "date": now_date,
                               "time": now_time,
                               "title": request.form['post_title'],
                               "text": entry_text,
                               "modified": now_date + ', ' + now_time})
        return render_template('add_entry.html', success=True)

    return render_template('add_entry.html')


def filter_entry_text(entry_text):
    regexp = re.compile(r'<div>')
    if regexp.search(entry_text) is not None and not entry_text.startswith('<div>'):
        entry_text = '<div>' + re.sub('<div>', '</div><div>', entry_text, 1)
    return entry_text


@app.route('/edit/<entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id=None):
    if request.method == 'POST':
        if 'edit-entry' in request.form:
            entry_text = filter_entry_text(request.form['entry_text'])
            now_date = time.strftime("%d/%m/%Y")
            now_time = time.strftime("%I:%M %p")
            db.entries.update_one({"_id": ObjectId(entry_id)},
                                  {"$set": {"title": request.form['entry_edit_title'],
                                            "text": entry_text,
                                            "modified": now_date + ', ' + now_time}})
        elif 'delete-entry' in request.form:
            delete_entry(entry_id)
    return redirect(url_for('show_entries'))


def delete_entry(entry_id=None):
    db.entries.delete_one({"_id": ObjectId(entry_id)})


@app.route('/show/<entry_id>', methods=['GET'])
def full_entry(entry_id=None):
    entry = None
    if request.method == 'GET':
        # print entry_id
        entries_coll = db.entries
        entry = entries_coll.find_one({"_id": ObjectId(entry_id)})
        if len(entry) != 0:
            entry = dict(id=entry['_id'],
                         author=entry['username'],
                         date=entry['date'],
                         time=entry['time'],
                         title=entry['title'],
                         text=entry['text'],
                         modified=entry['modified'])
    return render_template('full_entry.html', entry=entry)


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
            # TODO: is_logged_in
            session['logged_in'] = True
            session['username'] = username
            # flash('You were logged in')
            return redirect(url_for('show_entries'))

    return render_template('login.html', user_does_not_exist=user_does_not_exist)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
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


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(exception):
    pass


if __name__ == '__main__':
    app.run()
