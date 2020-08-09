# routes.py

from flask import render_template, Blueprint
from sqlalchemy import desc, asc
from .db_models import Users, Categories, Threads, Messages
from . import db

main = Blueprint('main', __name__)


# Main route that lists all categories
@main.route('/')
def index():
    categories = db.session.query(Categories).with_entities(Categories.category_id,
                                                            Categories.category_name,
                                                            Categories.category_description
                                                            )
    sum_threads = db.session.query(Threads).count()
    sum_messages = db.session.query(Messages).count()
    return render_template('categories.html',
                           categories = categories,
                           sum_threads = sum_threads,
                           sum_messages = sum_messages,
                           cateogry_threads = "2",
                           category_messages = '24'
                           )


# Route that lists all threads on selected category
@main.route('/<category_id>/')
def list_threads(category_id):
    print("LIST THREADS")
    category_info = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    threads = db.session.query(Threads).filter(Threads.category_id == category_info.category_id).all()
    return render_template('threads.html',
                           threads = threads,
                           category_info = category_info
                           )


# Route that lists all messages on selected thread
@main.route('/<category_id>/<thread_id>')
def list_messages(category_id, thread_id):
    print("LIST MESSAGES")
    messages = db.session.query(Messages, Threads) \
        .join(Users) \
        .filter(thread_id == Messages.thread_id) \
        .with_entities(Messages.message_content,
                       Messages.message_created,
                       Users.username) \
        .order_by(asc(Messages.message_created))
    thread_info = db.session.query(Threads).filter(Threads.thread_id == thread_id).first()
    return render_template('messages.html',
                           messages = messages,
                           thread_info = thread_info,
                           category_id = category_id
                           )
