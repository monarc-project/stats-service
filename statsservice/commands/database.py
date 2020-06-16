import click

from statsservice import models
from statsservice.bootstrap import application, db


@application.cli.command("db_empty")
def db_empty():
    """Drop all the database.
    """
    if click.confirm("Do you want to drop all the database?"):
        with application.app_context():
            models.db_empty(db)
            print("Database dropped.")


@application.cli.command("db_create")
def db_create():
    "Will create the database."
    with application.app_context():
        models.db_create(
            db,
            application.config["DB_CONFIG_DICT"],
            application.config["DATABASE_NAME"],
        )


@application.cli.command("db_init")
def db_init():
    "Will create the database from conf parameters."
    with application.app_context():
        models.db_init(db)
