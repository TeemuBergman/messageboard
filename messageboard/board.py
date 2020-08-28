# board.py

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
# From message board
from .user_roles import login_required, Role, check_secret
from .csrf import set_csrf_token, validate_csrf_token
from . import db

board = Blueprint("board", __name__)


# Search messages
@board.route("/results", methods = ["GET"])
def search_messages():
    # Check if user can view secret categories
    view_secret = check_secret()

    query = request.args["query"]

    # Check that query has content
    if query:
        sql = """
            SELECT
                c.category_id,
                c.category_name,
                c.category_secret,
                t.thread_id,
                (SELECT DISTINCT(t.thread_name)) as thread_name,
                m.message_content,
                m.message_created,
                u.username
            FROM threads AS t
            JOIN messages AS m ON m.thread_id = t.thread_id
            JOIN categories AS c ON c.category_id = t.category_id
            JOIN users AS u ON u.user_id = m.user_id
            WHERE c.category_secret IN (false, :category_secret)
            AND LOWER(m.message_content) LIKE LOWER(:query)
            ORDER BY c.category_id;
        """
        messages = db.session.execute(sql, {"query": "%" + query + "%",
                                            "category_secret": view_secret})
    else:
        messages = ""

    return render_template("search_results.html",
                           messages = messages)


# List categories
@board.route("/")
def index():
    # Set token
    set_csrf_token()

    # Check if user can view secret categories
    view_secret = check_secret()

    # Get categories (also secret ones if user has the rights) and count threads and messages
    sql = """
        SELECT
            c.category_id,
            c.category_name,
            c.category_description,
            COUNT(DISTINCT t.thread_id) AS threads_count,
            COUNT(DISTINCT m.message_id) AS messages_count
        FROM categories AS c
        FULL OUTER JOIN threads AS t ON c.category_id = t.category_id
        FULL OUTER JOIN messages AS m ON t.thread_id = m.thread_id
        WHERE c.category_secret IN (false, :category_secret)
        GROUP BY c.category_id, c.category_name, c.category_description
        ORDER BY c.category_id;
    """
    categories = db.session.execute(sql, {"category_secret": view_secret})

    # Count all threads
    sql = """
        SELECT COUNT(thread_id)
        FROM threads AS t
        JOIN categories AS c ON t.category_id = c.category_id
        WHERE c.category_secret IN (false, :category_secret);
    """
    sum_threads = db.session.execute(sql, {"category_secret": view_secret}).first()[0]

    # Count all messages
    sql = """
        SELECT COUNT(m.message_id)
        FROM messages AS m
        JOIN threads t ON m.thread_id = t.thread_id
        JOIN categories AS c ON t.category_id = c.category_id
        WHERE c.category_secret IN (false, :category_secret);;
    """
    sum_messages = db.session.execute(sql, {"category_secret": view_secret}).first()[0]

    # Count all users
    sql = """
        SELECT COUNT(user_id)
        FROM users
        WHERE NOT user_role = 'DELETED';
    """
    sum_users = db.session.execute(sql).first()[0]

    return render_template("categories.html",
                           categories = categories,
                           sum_threads = sum_threads,
                           sum_messages = sum_messages,
                           sum_users = sum_users,
                           user = current_user)


# New category (ADMIN)
@board.route("/new_category", methods = ["GET", "POST"])
@login_required(Role.ADMIN)
def index_new_category():
    # Validate token
    validate_csrf_token()

    # Get content from form...
    category_name = request.form["category_name"]
    category_description = request.form["category_description"]
    category_secret = request.form.get("category_secret")
    # ...and clean it
    category_name = remove_spaces(category_name)
    category_description = remove_spaces(category_description)

    if not category_secret:
        category_secret = "False"

    # Construct and send reply to database
    sql = """
            INSERT INTO categories (category_secret,
                                    category_name,
                                    category_description, 
                                    category_created)
            VALUES (:category_secret, :category_name, :category_description, :category_created);
        """
    db.session.execute(sql, {
        "category_secret": category_secret,
        "category_name": category_name,
        "category_description": category_description,
        "category_created": datetime.now()
    })
    db.session.commit()

    return redirect(request.referrer)


# List all threads on selected category
@board.route("/<int:category_id>/")
def list_threads(category_id):
    # Check if user can view secret categories
    view_secret = check_secret()

    # Get threads, count messages, username, last message and timestamp
    sql = """
        SELECT
            c.category_id,
            c.category_name,
            c.category_secret,
            t.thread_id,
            t.thread_name,
            t.thread_created,
            m1.message_content,
            (SELECT COUNT(m3.message_id) FROM messages AS m3 WHERE m3.thread_id = t.thread_id) AS messages_count,
            m1.message_created,
            u.username
        FROM messages m1
        LEFT JOIN threads AS t ON t.thread_id = m1.thread_id
        LEFT JOIN categories AS c ON c.category_id = t.category_id
        LEFT OUTER JOIN messages AS m2 ON m2.thread_id=m1.thread_id
        AND m2.message_created > m1.message_created
        LEFT JOIN users AS u ON m1.user_id = u.user_id
        WHERE m2.message_created IS NULL
        AND c.category_id = :category_id
        AND c.category_secret IN (false, :category_secret)
        ORDER BY m1.message_created DESC;
    """
    threads = db.session.execute(sql, {"category_id": category_id,
                                       "category_secret": view_secret})

    # Count all threads
    sql = """
        SELECT COUNT(thread_id)
        FROM threads AS t
        JOIN categories AS c ON t.category_id = c.category_id
        AND c.category_secret IN (false, :category_secret)
        AND c.category_id = :category_id;
    """
    sum_threads = db.session.execute(sql, {"category_id": category_id,
                                           "category_secret": view_secret}).first()[0]

    # Count all messages
    sql = """
        SELECT COUNT(message_id)
        FROM messages AS m
        JOIN threads t ON m.thread_id = t.thread_id
        JOIN categories c ON t.category_id = c.category_id
        WHERE c.category_id = :category_id
        AND c.category_secret IN (false, :category_secret);
    """
    sum_messages = db.session.execute(sql, {"category_id": category_id,
                                            "category_secret": view_secret}).first()[0]

    # Get category data
    category_row = get_category_row(category_id)

    return render_template("threads.html",
                           current_user = current_user,
                           threads = threads,
                           sum_threads = sum_threads,
                           sum_messages = sum_messages,
                           category_info = category_row,
                           viewable = view_secret
                           )


'''
    Message functions
'''


# List all messages on selected thread
@board.route("/<int:category_id>/<int:thread_id>")
def list_messages(category_id, thread_id):
    # Set token
    set_csrf_token()

    # Check if user can view secret categories
    view_secret = check_secret()

    # Get messages from database
    sql = """
        SELECT
            t.thread_id,
            t.thread_name,
            m.message_id,
            m.message_content,
            m.message_created,
            m.message_edited,
            u.user_id,
            u.username,
            u.deleted
        FROM messages m
        JOIN users AS u ON u.user_id = m.user_id
        JOIN threads AS t ON t.thread_id = m.thread_id
        JOIN categories AS c ON t.category_id = c.category_id
        WHERE c.category_secret IN (false, :category_secret)
        AND m.thread_id = :thread_id
        ORDER BY m.message_created;
    """
    messages = db.session.execute(sql, {"thread_id": thread_id,
                                        "category_secret": view_secret})

    thread_info = db.session.execute(sql, {"thread_id": thread_id,
                                           "category_secret": view_secret}).fetchone()

    category_info = get_category_row(category_id)

    return render_template("messages.html",
                           current_user = current_user,
                           messages = messages,
                           thread_info = thread_info,
                           category_info = category_info
                           )


# Post a new reply to a thread
@board.route("/<int:category_id>/<int:thread_id>/", methods = ["POST"])
@login_required(Role.USER)
def post_reply(category_id, thread_id):
    # Validate token
    validate_csrf_token()

    # Get content from form...
    content = request.form["content"]
    # ...and clean it
    content = remove_spaces(content)

    # Check if reply has too many characters
    if len(content) > 5000 or len(content) == 0:
        return redirect(request.referrer)

    # Construct and send reply to database
    sql = """
            INSERT INTO messages (message_content, thread_id, user_id, message_created)
            VALUES (:message_content, :thread_id, :user_id, :message_created);
        """
    db.session.execute(sql, {
        "message_content": content,
        "thread_id": thread_id,
        "user_id": current_user.user_id,
        "message_created": datetime.now()
    })
    db.session.commit()

    return redirect(request.referrer)


# Edit selected message
@board.route("/<int:category_id>/<int:thread_id>/edit", methods = ["POST"])
@login_required(Role.USER)
def edit_message(category_id, thread_id):
    if "edit_message" in request.form:
        # Validate token
        validate_csrf_token()

        # Get content...
        message_id = request.form["edit_message"]
        message_content = request.form["edit_content"]
        # ...and clean it
        message_content = remove_spaces(message_content)

        if message_content:
            sql = """
                UPDATE messages
                SET
                    message_content = :message_content,
                    message_edited = :timestamp
                WHERE message_id = :message_id
                AND user_id = :current_user;
            """
            db.session.execute(sql, {
                "message_content": message_content,
                "timestamp": datetime.now(),
                "message_id": message_id,
                "current_user": current_user.user_id
            })
            db.session.commit()

        return redirect(request.referrer)
    pass


# Delete selected message
@board.route("/<int:category_id>/<int:thread_id>/delete", methods = ["POST"])
@login_required(Role.USER)
def delete_message(category_id, thread_id):
    # Validate token
    validate_csrf_token()

    # Get message ID
    message_id = request.form["message_id"]

    # Delete message
    sql = """
        DELETE 
        FROM messages
        WHERE message_id = :message_id
        AND user_id = :current_user
    """
    db.session.execute(sql, {"message_id": message_id,
                             "current_user": current_user.user_id})
    db.session.commit()

    # Check if it was the last message in thread...
    sql = """
        SELECT COUNT(thread_id) as total
        FROM messages
        WHERE thread_id = :thread_id
    """
    # ...and return accordingly
    if db.session.execute(sql, {"thread_id": thread_id}).fetchone()[0] == 0:
        # Delete thread
        sql = """
            DELETE FROM threads
            WHERE thread_id = :thread_id;
        """
        db.session.execute(sql, {"thread_id": thread_id})
        db.session.commit()

        return redirect(url_for("board.list_threads",
                                category_id = category_id))
    else:
        return redirect(request.referrer)


# Delete selected message
@board.route("/<int:category_id>/<int:thread_id>/admin_delete_message", methods = ["POST"])
@login_required(Role.ADMIN)
def admin_delete_message(category_id, thread_id):
    # Validate token
    validate_csrf_token()

    # Get message ID
    message_id = request.form["message_id"]

    # "Delete" selected message (change message content)
    sql = """
        UPDATE messages
        SET
            message_content = '*** Message deleted by administrator ***',
            message_edited = :current_time
        WHERE message_id = :message_id;
    """

    db.session.execute(sql, {
        "username": current_user.username,
        "current_time": datetime.now(),
        "message_id": message_id
    })
    db.session.commit()

    return redirect(request.referrer)


# Delete selected message
@board.route("/<int:category_id>/<int:thread_id>/admin_delete_thread", methods = ["POST"])
@login_required(Role.ADMIN)
def admin_delete_thread(category_id, thread_id):
    # Validate token
    validate_csrf_token()

    # Delete all messages in thread
    sql = """
        DELETE
        FROM messages
        WHERE thread_id = :thread_id;
    """
    db.session.execute(sql, {"thread_id": thread_id})
    db.session.commit()

    # Delete the corresponding thread
    sql = """
        DELETE
        FROM threads
        WHERE thread_id = :thread_id;
    """
    db.session.execute(sql, {"thread_id": thread_id})
    db.session.commit()

    return list_threads(category_id)


'''
    Create new thread
'''


# Create a new thread
@board.route("/<int:category_id>/createthread")
@login_required(Role.USER)
def new_thread(category_id):
    # Set token
    set_csrf_token()
    return render_template("new_thread.html",
                           category_id = category_id)


# Send new thread to database
@board.route("/<int:category_id>/createthread", methods = ["POST"])
@login_required(Role.USER)
def new_thread_post(category_id):
    # Validate token
    validate_csrf_token()

    # Get content from form
    thread_name = request.form["thread_name"]
    content = request.form["content"]
    # ...and clean it
    thread_name = remove_spaces(thread_name)
    content = remove_spaces(content)

    # Check if reply has too many characters
    if len(thread_name) > 100 or len(thread_name) == 0:
        return redirect(request.referrer)
    if len(content) > 5000 or len(content) == 0:
        return redirect(request.referrer)

    # Construct a new thread and first post
    current_time = datetime.now()
    sql = """
        WITH new_thread
        AS (INSERT INTO threads (thread_name, category_id, thread_created)
        VALUES (:thread_name, :category_id, :thread_created)
        RETURNING thread_id)
        INSERT INTO messages (message_content, thread_id, user_id, message_created)
        VALUES (:message_content, (SELECT thread_id FROM new_thread), :user_id, :message_created);
    """

    db.session.execute(sql, {
        "thread_name": thread_name,
        "category_id": category_id,
        "thread_created": current_time,
        "message_content": content,
        "user_id": current_user.user_id,
        "message_created": current_time
    })
    db.session.commit()

    return redirect(url_for("board.list_threads",
                            category_id = category_id))


'''
    Shared functions
'''


# Get one row of selected category
def get_category_row(category_id):
    sql = """
        SELECT
            category_id,
            category_secret,
            category_name,
            category_description 
        FROM categories 
        WHERE category_id = :category_id;
    """
    result = db.session.execute(sql, {"category_id": category_id})
    return result.fetchone()


# Remove unnecessary spaces
def remove_spaces(messy_text):
    return '\n'.join(' '.join(line.split()) for line in messy_text.split('\n'))
