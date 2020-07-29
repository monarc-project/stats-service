import click
import secrets

from statsservice.bootstrap import application, db
from statsservice.models import Client


@application.cli.command("create_client")
@click.option("--name", required=True, help="Name of the client.")
@click.option("--uuid", default="", help="UUID of the client.")
@click.option("--token", default="", help="Token of the client.")
@click.option(
    "--role",
    default="user",
    help="Role of the client (user or admin).",
    show_default=True,
)
def create_client(name, uuid, token, role):
    """Create a new client.
    """
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


@application.cli.command("list_clients")
def list_clients():
    """List all local clients.
    """
    for client in Client.query.all():
        print(client)
        print()


@application.cli.command("delete_client")
@click.option("--uuid", default="", help="UUID of the client to delete.")
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically reply yes to the confirmation message for the deletion of the client.",
)
def delete_client(uuid, yes):
    """Delete the client specified with its UUID and all the related local stats.
    """
    if yes or click.confirm("Delete all local stats related to this client?"):
        try:
            Client.query.filter(Client.uuid == uuid).delete()
            db.session.commit()
        except Exception as e:
            print(e)
