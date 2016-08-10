from flask import render_template, request, session, redirect, url_for
from minBlog import app, db
from bson import ObjectId
import Helper
import time


# TODO error-handling
@app.route('/new', methods=['GET', 'POST'])
def add_entry():
    # if not session.get('logged_in'):
    #    abort(401)
    if request.method == 'POST':
        entry_text = request.form['entry_text']
        entry_text = Helper.filter_entry_text(entry_text)
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
                               "modified": now_date + ', ' + now_time,
                               "is_modified": False})
        return render_template('add_entry.html', success=True)

    return render_template('add_entry.html')


@app.route('/edit/<entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id=None):
    if request.method == 'POST':
        if 'edit-entry' in request.form:
            entry_text = Helper.filter_entry_text(request.form['entry_text'])
            if entry_text:
                now_date = time.strftime("%d/%m/%Y")
                now_time = time.strftime("%I:%M %p")
                db.entries.update_one({"_id": ObjectId(entry_id)},
                                      {"$set": {"title": request.form['entry_edit_title'],
                                                "text": entry_text,
                                                "modified": now_date + ', ' + now_time,
                                                "is_modified": True}})
        elif 'delete-entry' in request.form:
            delete_entry(entry_id)
    return redirect(url_for('show_user_entries'))


def delete_entry(entry_id=None):
    db.entries.delete_one({"_id": ObjectId(entry_id)})
