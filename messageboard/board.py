# board.py

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db

board = Blueprint("board", __name__)


# List categories
@board.route("/")
def index():
    # Check if current user can view secret categories
    if current_user.is_authenticated:
        sql = "SELECT view_secret " \
              "FROM users " \
              "WHERE user_id = :user_id;"
        category_secret = db.session.execute(sql, {"user_id": current_user.user_id}).first()[0]
    else:
        category_secret = False

    # Get categories and count threads and messages
    sql = "SELECT " \
          "c.category_id, " \
          "c.category_name, " \
          "c.category_description, " \
          "COUNT(DISTINCT t.thread_id) AS threads_count, " \
          "COUNT(DISTINCT m.message_id) AS messages_count " \
          "FROM categories AS c " \
          "JOIN threads AS t ON c.category_id = t.category_id " \
          "JOIN messages AS m ON t.thread_id = m.thread_id " \
          "WHERE c.category_secret = false " \
          "OR c.category_secret = :category_secret " \
          "GROUP BY c.category_id, c.category_name, c.category_description " \
          "ORDER BY c.category_name;"
    categories = db.session.execute(sql, {"category_secret": category_secret})

    # Count all threads
    sql = "SELECT COUNT(*) " \
          "FROM threads " \
          "WHERE thread_visible = true;"
    sum_threads = db.session.execute(sql).first()[0]

    # Count all messages
    sql = "SELECT COUNT(m.message_id) " \
          "FROM messages AS m " \
          "JOIN threads t on m.thread_id = t.thread_id " \
          "WHERE t.thread_visible = true;"
    sum_messages = db.session.execute(sql).first()[0]

    # Count all users
    sql = "SELECT COUNT(u.user_id) " \
          "FROM users AS u " \
          "WHERE u.deleted = false;"
    sum_users = db.session.execute(sql).first()[0]

    return render_template("categories.html",
                           categories = categories,
                           sum_threads = sum_threads,
                           sum_messages = sum_messages,
                           sum_users = sum_users,
                           user = current_user
                           )


# List all threads on selected category
@board.route("/<category_id>/")
def list_threads(category_id):
    category_info = get_category(category_id)

    # Get threads, count messages, username, last message and timestamp
    sql = "SELECT " \
          "t.category_id, " \
          "t.thread_id, " \
          "t.thread_name, " \
          "t.thread_created, " \
          "m1.message_content, " \
          "(SELECT COUNT(m3.message_id) FROM messages AS m3 " \
          "WHERE m3.thread_id = t.thread_id) AS messages_count, " \
          "m1.message_created, " \
          "u.username " \
          "FROM messages m1 " \
          "LEFT OUTER JOIN messages m2 ON m2.thread_id=m1.thread_id " \
          "AND m2.message_created > m1.message_created " \
          "LEFT JOIN threads t ON t.thread_id = m1.thread_id " \
          "LEFT JOIN users u ON m1.user_id = u.user_id " \
          "WHERE m2.message_created IS NULL " \
          "AND t.thread_visible = true " \
          "AND t.category_id = :category_id " \
          "ORDER BY m1.message_created DESC;"
    threads = db.session.execute(sql, {"category_id": category_id})

    return render_template("threads.html",
                           threads = threads,
                           category_info = category_info
                           )


# List all messages on selected thread
@board.route("/<category_id>/<thread_id>", methods = ["GET", "POST"])
def list_messages(category_id, thread_id):
    category_info = get_category(category_id)

    # Get messages from database
    sql = "SELECT t.thread_id, " \
          "t.thread_name, " \
          "m.message_id, " \
          "m.message_content, " \
          "m.message_created, " \
          "m.message_edited, " \
          "u.user_id, " \
          "u.username, " \
          "u.deleted " \
          "FROM messages m " \
          "JOIN users u on u.user_id = m.user_id " \
          "JOIN threads t on t.thread_id = m.thread_id " \
          "WHERE m.thread_id = :thread_id " \
          "AND m.deleted = False " \
          "ORDER BY m.message_created;"
    messages = db.session.execute(sql, {"thread_id": thread_id})
    thread_info = db.session.execute(sql, {"thread_id": thread_id}).fetchone()

    if request.method == "POST":
        # Execute delete button
        if "delete_message" in request.form:
            message_id = request.form["message_id"]
            thread_id = request.form["thread_id"]
            deleted = delete_message(thread_id, message_id)
            if deleted:
                return redirect(url_for("board.list_threads",
                                        category_id = category_id
                                        ))
            else:
                return redirect(request.referrer)

        # Execute edit button
        if "edit_message" in request.form:
            message_id = request.form["edit_message"]
            message_content = request.form["edit_content"]
            edit_message(message_id, message_content)
            return redirect(request.referrer)

    return render_template("messages.html",
                           messages = messages,
                           thread_info = thread_info,
                           category_info = category_info,
                           current_user = current_user
                           )


# Create a new thread
@board.route("/<category_id>/createthread")
@login_required
def new_thread(category_id):
    return render_template("new_thread.html",
                           category_id = category_id
                           )


# Send new thread info to database
@board.route("/<category_id>/createthreadpost", methods = ["POST"])
@login_required
def new_thread_post(category_id):
    # Get content from form
    thread_name = request.form["thread_name"]
    content = request.form["content"]

    # Check if reply has too many characters
    if len(thread_name) > 100 or len(thread_name) == 0:
        return redirect(request.referrer)
    if len(content) > 5000 or len(content) == 0:
        return redirect(request.referrer)

    # Construct a new thread and first post
    current_time = datetime.now()
    sql = "WITH new_thread " \
          "AS (INSERT INTO threads (thread_name, category_id, thread_created) " \
          "VALUES (:thread_name, :category_id, :thread_created) " \
          "RETURNING thread_id) " \
          "INSERT INTO messages (message_content, thread_id, user_id, message_created) " \
          "VALUES (:message_content, (SELECT thread_id FROM new_thread), :user_id, :message_created);"

    db.session.execute(sql, {"thread_name": thread_name,
                             "category_id": category_id,
                             "thread_created": current_time,
                             "message_content": content,
                             "user_id": current_user.user_id,
                             "message_created": current_time
                             })
    db.session.commit()
    db.session.close()

    return redirect(url_for("board.list_threads",
                            category_id = category_id
                            ))


# Post a new reply to a thread
@board.route("/<category_id>/<thread_id>/reply", methods = ["POST"])
@login_required
def post_reply(category_id, thread_id):
    # Get content from form
    content = request.form["content"]

    # Check if reply has too many characters
    if len(content) > 5000 or len(content) == 0:
        return redirect(request.referrer)

    # Construct and send reply to database
    sql = "INSERT INTO messages (message_content, thread_id, user_id, message_created)" \
          "VALUES (:message_content, :thread_id, :user_id, :message_created);"
    db.session.execute(sql, {"message_content": content,
                             "thread_id": thread_id,
                             "user_id": current_user.user_id,
                             "message_created": datetime.now()
                             })
    db.session.commit()
    db.session.close()

    return redirect(request.referrer)


# Delete selected message
@login_required
def delete_message(thread_id, message_id):
    # Delete selected message
    sql = "DELETE FROM messages " \
          "WHERE message_id = :message_id " \
          "AND user_id = :current_user;"
    db.session.execute(sql, {"message_id": message_id,
                             "current_user": current_user.user_id})
    db.session.commit()
    db.session.close()

    # Check if it was last message on thread
    sql = "SELECT COUNT(thread_id) as total " \
          "FROM messages " \
          "WHERE thread_id = :thread_id"
    # Return accordingly
    if db.session.execute(sql, {"thread_id": thread_id}).fetchone() == 0:
        return True
    else:
        return False


# Edit selected message
@login_required
def edit_message(message_id, message_content):
    # Change deleted value to True
    sql = "UPDATE messages " \
          "SET message_content = :message_content, message_edited = :timestamp " \
          "WHERE message_id = :message_id " \
          "AND user_id = :current_user;"
    db.session.execute(sql, {"message_content": message_content,
                             "timestamp": datetime.now(),
                             "message_id": message_id,
                             "current_user": current_user.user_id})
    db.session.commit()
    db.session.close()


# Get one row of selected category
def get_category(category_id):
    sql = "SELECT * FROM categories " \
          "WHERE category_id = :category_id;"
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchone()
