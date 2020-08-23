# routes.py

import os
from flask import Blueprint, send_from_directory, redirect, url_for

main = Blueprint("main", __name__)


# Get favicon.ico
@main.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(main.root_path, "static"),
                               "favicon.ico", mimetype = "image/vnd.microsoft.icon")


# Main route that lists all categories
@main.route("/")
def index():
    return redirect(url_for("board.index"))
