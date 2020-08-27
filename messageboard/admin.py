# admin.py

from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import current_user
from user_roles import login_required, Role
from messageboard import db

admin_auth = Blueprint("admin_auth", __name__)


# Admin control panel
@admin_auth.route("/", methods = ["GET", "POST"])
@login_required(Role.ADMIN)
def control_panel():
    if request.method == "POST":
        # Save edit to user profile
        admin = request.form.get("admin")
        view_secret = request.form.get("view_secret")
        deleted = request.form.get("deleted")
        banned = request.form.get("banned")
        user_id = request.form["save_changes"]

        # Update user privileges
        sql = """
              UPDATE users
              SET admin = :admin, view_secret = :view_secret, banned = :banned, deleted = :deleted
              WHERE user_id = :user_id; 
              """
        db.session.execute(sql, {
            "user_id": user_id,
            "admin": admin,
            "view_secret": view_secret,
            "banned": banned,
            "deleted": deleted
        })
        db.session.commit()

    return render_template("/admin/admin.html",
                           users = get_users())


# Admin control panel
@admin_auth.route("/users", methods = ["GET", "POST"])
@login_required(Role.ADMIN)
def edit_users():
    return render_template("/admin/users.html",
                           users = get_users())


# Get all categories
def get_all_categories():
    sql = """
          SELECT
          category_id,
          category_name,
          category_description,
          category_secret,
          category_created
          FROM categories 
          ORDER BY category_name;
          """
    return db.session.execute(sql)


# Create a new category
def new_category(category_secret, category_name, category_description):
    sql = """
          INSERT INTO categories (category_secret, category_name, category_description, category_created)
          VALUES (:category_secret, :category_name, :category_description, :category_created);
          """
    db.session.execute(sql, {"category_secret": category_secret,
                             "category_name": category_name,
                             "category_description": category_description,
                             "category_created": datetime.now()})
    db.session.commit()


# Delete category
def delete_category(category_id):
    sql = """
          DELETE FROM categories
          WHERE category_id = :category_id
          """
    db.session.execute(sql, {"category_id": category_id})


# Set category secret status -switch
def switch_category_secret(category_id):
    sql = """
          SELECT category_secret
          FROM categories
          WHERE category_id = :category_id
          """
    category_secret = db.session.execute(sql, {"category_id": category_id})

    # Set new banned status
    sql = """
          UPDATE categories
          SET category_secret = :category_secret
          WHERE category_id = :category_id;
          """
    db.session.execute(sql, {"category_id": category_id,
                             "category_secret": category_secret})
    db.session.commit()


# Get all threads of specific category
def get_threads(category_id):
    sql = """
          SELECT
          thread_id,
          thread_name,
          thread_created,
          category_id
          FROM threads
          WHERE category_id = :category_id
          ORDER BY thread_name;
          """
    return db.session.execute(sql, {"category_id": category_id})


# Get all users
def get_users():
    sql = """
          SELECT
          user_id,
          username,
          password_hash,
          email,
          account_created,
          last_login,
          banned,
          ban_duration,
          admin,
          view_secret,
          deleted,
          user_role
          FROM users
          ORDER BY username;
          """
    return db.session.execute(sql)


# Ban or lift ban -switch
def switch_ban_user(user_id):
    # Get current banned status and flip it
    banned = not current_user.banned

    # Set new banned status
    sql = """
          UPDATE users
          SET banned = :banned
          WHERE user_id = :user_id;
          """
    db.session.execute(sql, {"user_id": user_id,
                             "banned": banned})
    db.session.commit()


# Delete or restore user -switch
def switch_delete_user(user_id):
    # Get current deleted status and flip it
    deleted = not current_user.banned

    # Set new deleted status
    sql = """
          UPDATE users
          SET deleted = :deleted
          WHERE user_id = :user_id;
          """
    db.session.execute(sql, {"user_id": user_id,
                             "banned": deleted})
    db.session.commit()


# Allow user to view secret categories -switch
def switch_user_view_secrets(user_id):
    # Get current view secrets status and flip it
    view_secret = not current_user.view_secret

    # Set new banned status
    sql = """
          UPDATE users
          SET view_secret = :view_secret
          WHERE user_id = :user_id;
          """
    db.session.execute(sql, {"user_id": user_id,
                             "view_secret": view_secret})
    db.session.commit()
