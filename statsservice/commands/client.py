import click
import secrets

from statsservice.bootstrap import application, db
from statsservice.models import Client


@application.cli.command("create_client")
@click.option("--name", required=True, help="Client name")
@click.option("--uuid", default="", help="Client UUID")
@click.option(
    "--role",
    default="user",
    help="Role of the client (user or admin)",
    show_default=True,
)
def create_client(name, uuid, role):
    """Create an client.
    """
    args = {}
    token = secrets.token_urlsafe(64)
    if uuid:
        args["uuid"] = uuid
    args.update(
        {
            "name": name,
            "token": token,
            "is_active": True,
            "role": (1 if role == "user" else 2),
        }
    )
    new_client = Client(**args)
    db.session.add(new_client)
    db.session.commit()
    print(new_client)


@application.cli.command("list_clients")
def list_clients():
    """List clients.
    """
    for client in Client.query.all():
        print(client)
        print()
