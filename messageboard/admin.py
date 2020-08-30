# admin.py

from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import current_user
# From message board app
from .user_roles import login_required, Role
from . import db

admin_auth = Blueprint("admin_auth", __name__)


# Admin control panel
@admin_auth.route("/", methods = ["GET", "POST"])
@login_required(Role.ADMIN)
def control_panel():
    if request.method == "POST":
        # Get edits to user profile
        user_role = request.form["user_role"]
        user_id = request.form["user_id"]

        # Update user privileges
        sql = """
              UPDATE users
              SET user_role = :user_role
              WHERE user_id = :user_id; 
              """
        db.session.execute(sql, {"user_id": user_id,
                                 "user_role": user_role})
        db.session.commit()

    return render_template("/admin/admin.html",
                           users = get_users())


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
