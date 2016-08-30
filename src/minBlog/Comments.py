from flask import request, jsonify, redirect, url_for
from minBlog import app, paginator, db
import time
from operator import itemgetter
from bson import ObjectId

@app.route('/submit_comment', methods=['GET'])
def submit_comment():
    entry_id = request.args.get('entry_id', '')
    new_comment = request.args.get('new_comment', '')
    commenter = request.args.get('commenter', '')
    now_date = time.strftime("%d/%m/%Y")
    now_time = time.strftime("%I:%M %p")
    db.comments.insert_one({"commenter": commenter,
                            "entry_id": entry_id,
                            "comment": new_comment,
                            "date": now_date,
                            "time": now_time,
                            "modified": now_date + ', ' + now_time,
                            "is_modified": False})
    latest_comment_in_db = db.comments.find({"entry_id": entry_id}).sort([("_id", -1)]).limit(1)  # descending order
    latest_comment_id = -1
    for latest_comment in latest_comment_in_db:
        latest_comment_id = str(latest_comment['_id'])
    latest_comment = dict(
        id=latest_comment_id,
        commenter=commenter,
        entry_id=entry_id,
        comment=new_comment,
        date=now_date,
        time=now_time,
        modified=now_date + ', ' + now_time,
        is_modified=False
    )
    paginator.repopulate_comments(latest_comment, entry_id)
    return jsonify(latest_comment=latest_comment, has_more_comments=paginator.has_more_comments(entry_id))


@app.route('/load_more_comments', methods=['GET'])
def load_more_comments():
    entry_id = request.args.get('entry_id', '')
    return jsonify(comments=paginator.load_more_comments(entry_id),
                   has_more_comments=paginator.has_more_comments(entry_id))


@app.route('/sort_comments', methods=['GET'])
def sort_comments():
    entry_id = request.args.get('entry_id', '')
    sort_by = request.args.get('sort_by', '')
    if sort_by == 'desc':
        sort_by = True
    else:
        sort_by = False
    unsorted_comments = paginator.get_comments(entry_id)
    #print unsorted_comments
    sorted_comments = sorted(unsorted_comments, key=itemgetter('id'), reverse=sort_by)
    #print sorted_comments
    paginator.populate_comments(sorted_comments, entry_id)
    return jsonify(comments=paginator.load_more_comments(entry_id),
                   has_more_comments=paginator.has_more_comments(entry_id))

@app.route('/edit_comment', methods=['POST'])
def edit_comment():
    entry_id = request.args.get('entry_id', '')
    comment_id = request.args.get('comment_id', '')
    updated_comment = request.args.get('updated_comment', '')

    now_date = time.strftime("%d/%m/%Y")
    now_time = time.strftime("%I:%M %p")
    db.comments.update_one({"_id": ObjectId(comment_id)},
                           {"$set": {"comment": updated_comment,
                                     "modified": now_date + ', ' + now_time,
                                     "is_modified": True}})
    return redirect(url_for('full_entry.html', entry_id=entry_id))
