import click
import secrets

from statsservice.bootstrap import application, db
from statsservice.models import Client


@application.cli.command("create_client")
@click.option("--name", required=True, help="Client name")
@click.option("--uuid", default="", help="Client UUID")
@click.option("--token", default="", help="Client token")
@click.option(
    "--role",
    default="user",
    help="Role of the client (user or admin)",
    show_default=True,
)
def create_client(name, uuid, token, role):
    """Create an client.
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
    """List clients.
    """
    for client in Client.query.all():
        print(client)
        print()
