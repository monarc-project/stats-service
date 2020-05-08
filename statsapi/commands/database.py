
import click

from mongoengine.connection import _get_db
from statsapi.bootstrap import application


@application.cli.command("drop_all_collections")
def drop_all_collections():
    """Drop all collections from the database.
    """
    if click.confirm('Do you want to drop all collections?'):
        db = _get_db()
        db.stats.drop()
        db.organization.drop()
        print("All collections dropped.")
