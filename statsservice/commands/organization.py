import click
import secrets

from statsservice.bootstrap import application, db
from statsservice.models import Organization


@application.cli.command("create_organization")
@click.option("--name", default="", help="Organization name (or UUID)")
def create_organization(name):
    """Create an organization.
    """
    token = secrets.token_urlsafe(64)
    new_org = Organization(name=name, token=token)
    db.session.add(new_org)
    db.session.commit()
    print(new_org)


@application.cli.command("list_organizations")
def list_organizations():
    """List organizations.
    """
    for organization in Organization.query.all():
        print(organization)
        print()
