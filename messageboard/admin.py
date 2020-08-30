# admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
# From message board app
from .csrf import set_csrf_token, validate_csrf_token
from .user_roles import login_required, Role
from . import db

admin_auth = Blueprint("admin_auth", __name__)


# Admin control panel
@admin_auth.route("/")
@login_required(Role.ADMIN)
def control_panel():
    # Set token
    set_csrf_token()

    # Get and show alert messages
    alert_message = request.args.get('alert_message')
    alert_type = request.args.get('alert_type')
    if alert_message:
        flash(alert_message, alert_type)

    # Get users profiles
    sql = """
          SELECT
            user_id,
            username,
            password_hash,
            email,
            user_role,
            account_created,
            last_login,
            ban_duration
          FROM users
          ORDER BY username;
          """
    users = db.session.execute(sql)

    return render_template("/admin/admin.html",
                           users = users)


# Admin control panel
@admin_auth.route("/", methods = ["POST"])
@login_required(Role.ADMIN)
def save_user_role():
    # Validate token
    validate_csrf_token()

    # Get edits to user profile
    user_role = request.form.get("user_role")
    user_id = request.form.get("user_id")

    # Update user privileges
    sql = """
          UPDATE users
          SET user_role = :user_role
          WHERE user_id = :user_id; 
          """
    db.session.execute(sql, {"user_id": user_id,
                             "user_role": user_role})
    db.session.commit()

    alert_message = "User role saved successfully!"
    alert_type = "alert-success"

    return redirect(url_for("admin_auth.control_panel",
                            alert_message = alert_message,
                            alert_type = alert_type))
