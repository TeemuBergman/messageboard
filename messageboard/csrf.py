# csrf.py

from os import urandom

# Set CSRF token
from flask import session, request, abort


def set_csrf_token():
    # Set CSRF token
    session["csrf_token"] = urandom(32).hex()


# Check that both CSRF tokens match
def validate_csrf_token():
    print(session["csrf_token"])
    print(request.form["csrf_token"])
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
