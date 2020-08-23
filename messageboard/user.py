# user.py

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .db_models import Users
from . import db

user_auth = Blueprint("user_auth", __name__)


# User login
@user_auth.route("/login")
def login():
    return render_template("login.html")


@user_auth.route("/login", methods = ["GET", "POST"])
def login_post():
    # Get login info from form
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # Get current user object
    user = Users.query.filter_by(email = email).first()

    # Look for the user and check password hash match and redirect if they don"t
    if not user:
        flash("Wrong email. \n Please try again!")
        return redirect(url_for("user_auth.login"))
    if not check_password_hash(user.password_hash, password):
        flash("Wrong password. \n Please try again!")
        return redirect(url_for("user_auth.login"))
    if user.deleted:
        flash("User account deleted!")
        return redirect(url_for("user_auth.login"))

    # Log in user
    login_user(user, remember = remember)

    # Update last login date and time
    sql = "UPDATE users " \
          "SET last_login = :time " \
          "WHERE user_id = :user_id;"
    db.session.execute(sql, {"time": datetime.now(),
                             "user_id": user.user_id})
    db.session.commit()
    db.session.close()

    return redirect(url_for("main.index"))


# User sign up
@user_auth.route("/signup")
def signup():
    return render_template("signup.html")


@user_auth.route("/signup", methods = ["POST"])
def signup_post():
    # Get user info from form
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if sign up has too many characters
    if len(username) > 100 or len(username) == 0:
        return redirect(request.referrer)
    if len(email) > 5000 or len(email) == 0:
        return redirect(request.referrer)
    if len(password) > 5000 or len(password) == 0:
        return redirect(request.referrer)

    # Check for email address already in database
    user = Users.query.filter_by(email = email).first()
    if user:
        flash("User with this email already exists.\n Please try again!")
        return redirect(url_for("user_auth.signup"))

    # Create new user data and add it to the database
    current_time = datetime.now()
    sql = "INSERT INTO users (username, email, password_hash, account_created, last_login)" \
          "VALUES (:username, :email, :password_hash, :account_created, :last_login);"
    db.session.execute(sql, {"username": username,
                             "email": email,
                             "password_hash": generate_password_hash(password, method = "sha256"),
                             "account_created": current_time,
                             "last_login": current_time
                             })
    db.session.commit()
    db.session.close()

    return redirect(url_for("user_auth.login"))


# User logout
@user_auth.route("/Logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# Route where logged user can view and edit its info
@user_auth.route("/profile", methods = ["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile.html",
                               username = current_user.username,
                               email = current_user.email,
                               banned = current_user.banned,
                               ban_duration = current_user.ban_duration,
                               registered = current_user.account_created,
                               last_login = current_user.last_login,
                               confirmation = False
                               )

    if request.method == "POST":

        if "delete_profile" in request.form:
            # Change deleted value to True
            sql = "UPDATE users " \
                  "SET deleted = true " \
                  "WHERE user_id = :user_id;"
            db.session.execute(sql, {"user_id": current_user.user_id})
            db.session.commit()
            db.session.close()

            # Log out user
            return redirect(url_for("user_auth.logout"))

        if "edit_profile" in request.form:
            # Check that the old password is valid
            password = request.form["password"]
            if password == "" or not check_password_hash(current_user.password_hash, password):
                pass
            else:
                # Check that email is valid
                email = request.form["email_1"]
                email_2 = request.form["email_2"]
                if email == "" or email != email_2:
                    email = current_user.email

                # Check that password is valid
                new_password_1 = request.form["new_password_1"]
                new_password_2 = request.form["new_password_2"]
                if new_password_1 == "" or new_password_1 != new_password_2:
                    password = current_user.password_hash
                else:
                    password = generate_password_hash(new_password_1, method = "sha256")

                # Update new user profile to DB
                sql = "UPDATE users " \
                      "SET email = :email, password_hash = :password " \
                      "WHERE user_id = :user_id;"
                db.session.execute(sql, {"email": email,
                                         "password": password,
                                         "user_id": current_user.user_id})
                db.session.commit()
                db.session.close()

            # Refresh profile page
            return redirect(request.referrer)
