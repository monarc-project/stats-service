import secrets
import sys

import click

from statsservice.bootstrap import application
from statsservice.bootstrap import db
from statsservice.models import Client


@application.cli.command("client_create")
@click.option("--name", required=True, help="Name of the client.")
@click.option("--uuid", default="", help="UUID of the client.")
@click.option("--token", default="", help="Token of the client.")
@click.option(
    "--role",
    default="user",
    help="Role of the client (user or admin).",
    show_default=True,
)
def client_create(name, uuid, token, role):
    """Create a new local client."""
    args = {}
    if uuid:
        args["uuid"] = uuid
    if not token:
        token = secrets.token_urlsafe(64)
    args.update(
        {
            "name": name,
            "token": token,
            "is_active": True,
            "role": (1 if role == "user" else 2),
        }
    )
    try:
        new_client = Client(**args)
        db.session.add(new_client)
        db.session.commit()
        print(new_client)
    except Exception as e:
        print(e)


@application.cli.command("client_list")
def client_list():
    """List all local clients."""
    for client in Client.query.all():
        print(client)
        print()


@application.cli.command("client_delete")
@click.option("--uuid", default="", help="UUID of the client to delete.")
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically reply yes to the confirmation message.",
)
def client_delete(uuid, yes):
    """Delete the client specified with its UUID and all the related local stats."""
    if yes or click.confirm("Delete all local stats related to this client?"):
        try:
            cl = Client.query.filter(Client.uuid == uuid).first()
            if cl:
                db.session.delete(cl)
                db.session.commit()
            else:
                print("No such client.", file=sys.stderr)
        except Exception as e:
            print(e)


@application.cli.command("client_coordinates_set")
@click.option("--uuid", required=True, help="UUID of the client.")
@click.option("--latitude", required=True, help="Latitude of the client.")
@click.option("--longitude", required=True, help="Longitude of the client.")
def client_coordinates_set(uuid, latitude, longitude):
    """Set the coordinates of the client specified with its UUID."""
    cl = Client.query.filter(Client.uuid == uuid).first()
    if not cl:
        print("No such client.", file=sys.stderr)
        return
    cl.latitude = latitude
    cl.longitude = longitude
    db.session.add(cl)
    db.session.commit()


@application.cli.command("client_coordinates_unset")
@click.option("--uuid", required=True, help="UUID of the client.")
def client_coordinates_unset(uuid):
    """Unset the coordinates of the client specified with its UUID."""
    cl = Client.query.filter(Client.uuid == uuid).first()
    if not cl:
        print("No such client.", file=sys.stderr)
        return
    cl.latitude = None
    cl.longitude = None
    db.session.add(cl)
    db.session.commit()


@application.cli.command("client_sharing_activate")
@click.option("--uuid", required=True, help="UUID of the client.")
def client_sharing_activate(uuid):
    """Set the is_sharing_enabled attribute of a local client, specified with its UUID, to True."""
    cl = Client.query.filter(Client.uuid == uuid, Client.local == True).first()  # noqa
    if not cl:
        print("No such client.", file=sys.stderr)
        return
    cl.is_sharing_enabled = True
    db.session.add(cl)
    db.session.commit()


@application.cli.command("client_sharing_deactivate")
@click.option("--uuid", required=True, help="UUID of the client.")
def client_sharing_deactivate(uuid):
    """Set the is_sharing_enabled attribute of a local client, specified with its UUID, to False."""
    cl = Client.query.filter(Client.uuid == uuid, Client.local == True).first()  # noqa
    if not cl:
        print("No such client.", file=sys.stderr)
        return
    cl.is_sharing_enabled = False
    db.session.add(cl)
    db.session.commit()
