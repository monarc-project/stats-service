import click
import secrets

from statsapi.bootstrap import application
from statsapi.documents import Organization


@application.cli.command("create_organization")
@click.option("--name", default="", help="Organization name (or UUID)")
def create_organization(name):
    """Create an organization.
    """
    token = secrets.token_urlsafe(64)
    new_org = Organization(name=name, token=token)
    new_org.save()
    print(new_org)
