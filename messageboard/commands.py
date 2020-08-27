# commands.py

# CLI command for creating demo data
import click
from flask.cli import with_appcontext

# From message board
from .db_models import Users, Categories, Threads, Messages
from .create_demodata import general, coding, secret, admin, john_doe, jane_doe
from . import db


# CLI command for DB initialize
@click.command("init-db")
@with_appcontext
def init_db():
    # Commit to DB
    db.create_all()
    # Print
    click.echo("Initialized the database.")


@click.command("demo-data")
@with_appcontext
def demo_data():
    # Categories
    db.session.add(general)
    db.session.add(coding)
    db.session.add(secret)
    # Users
    db.session.add(admin)
    db.session.add(john_doe)
    db.session.add(jane_doe)
    # Commit
    db.session.commit()
    # Print
    click.echo("Demodata created!")
