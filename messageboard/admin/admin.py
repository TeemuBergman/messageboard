# admin.py

import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from messageboard import db

admin_auth = Blueprint("admin_auth", __name__)


# Admin control panel
@admin_auth.route("/", methods = ["GET", "POST"])
@login_required
def admin_control_panel():
    if current_user.is_admin:
        return render_template("/admin/admin.html")
    else:
        return redirect(url_for("main.index"))


# Get all categories
def get_all_categories():
    sql = "SELECT * " \
          "FROM categories " \
          "ORDER BY category_name;"
    return db.session.execute(sql)


# Create a new category
def new_category(category_secret, category_name, category_description):
    sql = "INSERT INTO categories (category_secret, category_name, category_description, category_created)" \
          "VALUES (:category_secret, :category_name, :category_description, :category_created);"
    db.session.execute(sql, {"category_secret": category_secret,
                             "category_name": category_name,
                             "category_description": category_description,
                             "category_created": datetime.datetime.now()
                             })
    db.session.commit()
    db.session.close()


# Delete category
def delete_category(category_id):
    sql = "DELETE FROM categories " \
          "WHERE category_id = :category_id"
    db.session.execute(sql, {"category_id": category_id})


# Set category secret status -switch
def switch_category_secret(category_id):
    sql = "SELECT category_secret " \
          "FROM categories " \
          "WHERE category_id = :category_id;"
    category_secret = db.session.execute(sql, {"category_id": category_id})

    # Set new banned status
    sql = "UPDATE categories " \
          "SET category_secret = :category_secret " \
          "WHERE category_id = :category_id;"
    db.session.execute(sql, {"category_id": category_id,
                             "category_secret": category_secret})
    db.session.commit()
    db.session.close()


# Get all threads of specific category
def get_threads(category_id):
    sql = "SELECT * " \
          "FROM threads " \
          "WHERE category_id = :category_id " \
          "ORDER BY thread_name;"
    return db.session.execute(sql, {"category_id": category_id})


# Get all users
def get_users():
    sql = "SELECT * " \
          "FROM users " \
          "ORDER BY username;"
    return db.session.execute(sql)


# Ban or lift ban -switch
def switch_ban_user(user_id):
    # Get current banned status and flip it
    banned = not current_user.banned

    # Set new banned status
    sql = "UPDATE users " \
          "SET banned = :banned " \
          "WHERE user_id = :user_id;"
    db.session.execute(sql, {"user_id": user_id,
                             "banned": banned})
    db.session.commit()
    db.session.close()


# Delete or restore user -switch
def switch_delete_user(user_id):
    # Get current deleted status and flip it
    deleted = not current_user.banned

    # Set new deleted status
    sql = "UPDATE users " \
          "SET deleted = :deleted " \
          "WHERE user_id = :user_id;"
    db.session.execute(sql, {"user_id": user_id,
                             "banned": deleted})
    db.session.commit()
    db.session.close()


# Allow user to view secret categories -switch
def switch_user_view_secrets(user_id):
    # Get current view secrets status and flip it
    can_view_secret = not current_user.can_view_secret

    # Set new banned status
    sql = "UPDATE users " \
          "SET can_view_secret = :can_view_secret " \
          "WHERE user_id = :user_id;"
    db.session.execute(sql, {"user_id": user_id,
                             "can_view_secret": can_view_secret})
    db.session.commit()
    db.session.close()
