import json
import click

from statsservice.lib import mosp
from statsservice.bootstrap import application


@application.cli.command("mosp_is_object_published")
@click.option("--uuid", required=True, help="UUID of the object.")
@click.option("-v", "--verbose", count=True, help="Display the object.")
def mosp_is_object_published(uuid, verbose):
    """Check if an object has been published on MOSP. Returns a boolean."""
    result = mosp.is_object_published(uuid, verbose != 0)
    print(result)
