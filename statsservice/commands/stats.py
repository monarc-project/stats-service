import json
import click
import requests

from urllib.parse import urljoin
from statsservice.bootstrap import application, db
from statsservice.models import Stats, Client

STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("stats_delete")
@click.option(
    "--client-uuid", default="", help="UUID of the client related to the stats."
)
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically reply yes to the confirmation message.",
)
def stats_delete(client_uuid, yes):
    """Delete the stats of a local client.
    """
    if yes or click.confirm("Delete all local stats related to this client?"):
        try:
            Stats.query.filter(Stats.client.has(uuid=client_uuid)).delete()
            db.session.commit()
        except Exception as e:
            print(e)


@application.cli.command("stats_push")
@click.option("--uuid", default="", help="Client uuid")
@click.option("--token", default="", help="Client token on remote side")
def stats_push(uuid, token):
    """Push stats for the client specified in parameter to an other stats
    server.
    """
    client = Client.objects.get(uuid__exact=uuid)

    headers = {"X-API-KEY": token, "content-type": "application/json"}

    payload = []
    stats = Stats.objects(client__exact=client)
    for stat in stats:
        payload.append(
            json.dumps(
                {
                    "uuid": str(stat.uuid),
                    "anr": str(stat.anr),
                    "type": stat.type,
                    "date": stat.date,
                    "data": stat.data,
                }
            )
        )

    try:
        print("Pushing stats for client {} {}".format(client.name))
        r = requests.post(STATS_API_ENDPOINT, data=payload, headers=headers)
        if r.status_code != 200:
            print("Impossible to push the stat.")
    except:
        pass


@application.cli.command("stats_pull")
@click.option("--uuid", default="", help="Client uuid")
def stats_pull(uuid):
    """Pull stats from an other stats instance for the client specified
    in parameter.
    """
    r = requests.get(STATS_API_ENDPOINT)
    stats = json.loads(r.content)
    for stat in stats["data"]:
        print(stat)
        # TODO: save the stat
