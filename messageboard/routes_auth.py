# routes_auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .db_models import Users, Threads, Messages
from . import db
from .tools import getTime

auth = Blueprint('auth', __name__)


# User login
@auth.route('/Login')
def login():
    return render_template('login.html')


@auth.route('/Login', methods = ['POST'])
def login_post():
    # Get login info from form
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email = email).first()

    # Look for the user and check password hash match and redirect if they don't
    if not user:
        flash('Wrong email. \n Please try again!')
        return redirect(url_for('auth.login'))
    if not check_password_hash(user.password_hash, password):
        flash('Wrong password. \n Please try again!')
        return redirect(url_for('auth.login'))

    login_user(user, remember = remember)

    return redirect(url_for('main.index'))


# User sign up
@auth.route('/Signup')
def signup():
    return render_template('signup.html')


@auth.route('/Signup', methods = ['POST'])
def signup_post():
    # Get user info from form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for email address already in database
    user = Users.query.filter_by(email = email).first()
    if user:
        flash('User with this email already exists.\n Please try again!')
        return redirect(url_for('auth.signup'))

    # Take current time with user data
    current_time = getTime()

    # Create new user data and add it to the database
    new_user = Users(
        username = username,
        email = email,
        password_hash = generate_password_hash(password, method = 'sha256'),
        account_created = current_time,
        last_login = current_time,
        is_admin = False,
        banned = False
    )

    # Database connection
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


# User logout
@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# Post a new message to a thread
@auth.route('/<category_id>/<thread_id>/Reply', methods = ["POST"])
@login_required
def post_reply(category_id, thread_id):
    print("POST REPLY")
    # Get content from form
    content = request.form["content"]

    # Check if reply has too many characters
    if len(content) > 5000:
        return redirect(url_for('main.index'))

    # Construct reply for database
    reply = Messages(message_content = content,
                     thread_id = thread_id,
                     user_id = current_user.user_id,
                     message_created = getTime()
                     )

    # Send reply to database
    db.session.add(reply)
    db.session.commit()
    return redirect(request.referrer)


# Create a new thread
@auth.route('/<category_id>/CreateThread')
@login_required
def new_thread(category_id):
    print("NEW THREAD")
    return render_template('new_thread.html',
                           category_id = category_id
                           )


# Send new thread info to database
@auth.route('/<category_id>/CreateThreadPost', methods = ["POST"])
@login_required
def new_thread_post(category_id):
    print("CREATED A NEW THREAD")
    # Get content from form
    thread_name = request.form["thread_name"]
    content = request.form["content"]

    # Check if reply has too many characters
    if len(thread_name) > 200:
        return redirect(request.referrer)
    if len(content) > 5000:
        return redirect(request.referrer)

    # Construct thread for database
    new_thread_data = Threads(thread_name = thread_name,
                     thread_visible = True,
                     category_id = category_id,
                     thread_created = getTime()
                     )
    db.session.add(new_thread_data)
    db.session.flush()

    # Construct reply for database
    new_post = Messages(message_content = content,
                     thread_id = new_thread_data.thread_id,
                     user_id = current_user.user_id,
                     message_created = getTime()
                     )

    # Send new thread to database
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('main.list_threads',
                            category_id = category_id
                            ))


# Route where logged user can view and edit its info
@auth.route('/Profile')
@login_required
def profile():
    return render_template('profile.html',
                           username = current_user.username,
                           email = current_user.email,
                           registered = current_user.account_created,
                           last_login = current_user.last_login
                           )