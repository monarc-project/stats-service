import json
import click

from statsservice.lib import mosp
from statsservice.bootstrap import application


@application.cli.command("is_object_published")
@click.option("--uuid", required=True, help="UUID of the object")
def is_object_published(uuid):
    """Check if an object has been published on MOSP. Returns a boolean."""
    result = mosp.is_object_published(uuid)
    print(result)
