# all the imports
from flask import Flask
from pymongo import MongoClient
import Paginator
import os

# configuration
DEBUG = True
#SECRET_KEY = '\xf6\x82R\xbeK\xa1QD\x03\xaa\x9a-\xd9\x1d\xc0$7XK\x0eo6\x1d\x05'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = os.urandom(32)
client = MongoClient()
db = client.flaskr
paginator = Paginator.Paginator(5, 5)


@app.before_request
def before_request():
    pass


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.teardown_request
def teardown_request(exception):
    pass


import minBlog.ViewEntries
import minBlog.EditEntries
import minBlog.User
import minBlog.Comments

if __name__ == '__main__':
    app.run()
