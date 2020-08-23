# init.py

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Init variables
db = SQLAlchemy()


# Page not found (404) handler
def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    app = Flask(__name__,
                instance_relative_config = False,
                template_folder = "templates",
                static_folder = "static")

    # Get config from config.py
    app.config.from_object("config.Config")

    # Init DB
    db.init_app(app)

    # User session manager and user_id loader
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .db_models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # All the elements of the message board
    with app.app_context():
        # Include routes
        from . import routes
        from . import board
        from . import user
        from . import admin

        # Register Blueprints
        # Main
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Admin
        from admin.admin import admin_auth as auth_admin_blueprint
        app.register_blueprint(auth_admin_blueprint, url_prefix = "/admin")

        # Authorised user
        from .user import user_auth as user_auth_blueprint
        app.register_blueprint(user_auth_blueprint)

        # Message board
        from .board import board as board_blueprint
        app.register_blueprint(board_blueprint, url_prefix = "/board")

        # Register page not found (404) handler
        app.register_error_handler(404, page_not_found)

        return app
