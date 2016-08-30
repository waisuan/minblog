from flask import render_template, request, session
from minBlog import app, paginator, db
from bson import ObjectId


@app.route('/')
@app.route('/<navigate>')
def show_all_entries(navigate=None):
    if navigate == 'next':
        all_entries = paginator.page_next(0)
    elif navigate == 'prev':
        all_entries = paginator.page_prev(0)
    else:
        entries_coll = db.entries
        all_entries = entries_coll.find().sort([("_id", -1)])  # ascending order
        paginator.insert(all_entries, 0)
        all_entries = paginator.page_next(0)
    has_more_pages = paginator.has_more_pages(0)
    has_prev_pages = paginator.has_prev_pages(0)
    entries = [dict(id=str(entry['_id']),
                    author=entry['username'],
                    date=entry['date'],
                    time=entry['time'],
                    title=entry['title'],
                    text=entry['text'],
                    modified=entry['modified']) for entry in all_entries]
    return render_template('show_entries.html', entries=entries,
                           has_more_pages=has_more_pages,
                           has_prev_pages=has_prev_pages,
                           all_entries=True)


@app.route('/user_entries')
@app.route('/user_entries/<navigate>')
def show_user_entries(navigate=None):
    curr_user = session['username']
    if navigate == 'next':
        all_entries = paginator.page_next(curr_user)
    elif navigate == 'prev':
        all_entries = paginator.page_prev(curr_user)
    else:
        entries_coll = db.entries
        all_entries = entries_coll.find({"username": curr_user}).sort([("_id", -1)])
        paginator.insert(all_entries, curr_user)
        all_entries = paginator.page_next(curr_user)
    # print all_entries
    has_more_pages = paginator.has_more_pages(curr_user)
    has_prev_pages = paginator.has_prev_pages(curr_user)
    entries = [dict(id=str(entry['_id']),
                    author=entry['username'],
                    date=entry['date'],
                    time=entry['time'],
                    title=entry['title'],
                    text=entry['text'],
                    modified=entry['modified'],
                    is_modified=entry['is_modified']) for entry in all_entries]
    return render_template('show_entries.html', entries=entries,
                           has_more_pages=has_more_pages,
                           has_prev_pages=has_prev_pages,
                           all_entries=False)


@app.route('/show/<entry_id>', methods=['GET'])
def full_entry(entry_id=None):
    entry = None
    if request.method == 'GET':
        # print entry_id
        entries_coll = db.entries
        entry = entries_coll.find_one({"_id": ObjectId(entry_id)})
        if len(entry) != 0:
            entry = dict(id=str(entry['_id']),
                         author=entry['username'],
                         date=entry['date'],
                         time=entry['time'],
                         title=entry['title'],
                         text=entry['text'],
                         modified=entry['modified'])
            all_comments_from_db = db.comments.find({"entry_id": entry_id})
            all_comments = []
            for comment in all_comments_from_db:
                all_comments.append(dict(
                    id=str(comment['_id']),
                    commenter=comment['commenter'],
                    entry_id=comment['entry_id'],
                    comment=comment['comment'],
                    date=comment['date'],
                    time=comment['time'],
                    modified=comment['modified'],
                    is_modified=comment['is_modified']
                ))
            paginator.populate_comments(all_comments, entry_id)
            entry['all_comments'] = paginator.load_more_comments(entry_id)
            entry['has_more_comments'] = paginator.has_more_comments(entry_id)
            # entry['all_comments'] = all_comments
    return render_template('full_entry.html', entry=entry)
