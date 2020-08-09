# init.py

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Init variables
db = SQLAlchemy()


# Page not found (404) handler
def page_not_found(e):
  return render_template('404.html'), 404


def create_app():
    app = Flask(__name__, instance_relative_config = False, template_folder = "templates", static_folder = "static")

    # Get config from config.py
    app.config.from_object('config.Config')

    db.init_app(app)

    # User session manager and user_id loader
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .db_models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # All the elements of the message board
    with app.app_context():
        # Include routes
        from . import routes
        from . import routes_auth
        # from .admin import admin

        # Register Blueprints
        from .routes_auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Register page not found (404) handler
        app.register_error_handler(404, page_not_found)

        return app
