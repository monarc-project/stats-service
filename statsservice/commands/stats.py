import json
import logging
import click
import requests
import sqlalchemy.exc

from urllib.parse import urljoin
from statsservice.bootstrap import application, db
from statsservice.models import Stats, Client


logger = logging.getLogger(__name__)


STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("stats_delete")
@click.option(
    "--client-uuid", default="", help="UUID of the lclient related to the stats."
)
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically reply yes to the confirmation message.",
)
def stats_delete(client_uuid, yes):
    """Delete the stats of a local client."""
    if yes or click.confirm("Delete all local stats related to this client?"):
        try:
            Stats.query.filter(Stats.client.has(uuid=client_uuid)).delete()
            db.session.commit()
        except Exception as e:
            print(e)


@application.cli.command("stats_push")
@click.option("--client-uuid", required=True, help="Local client uuid")
@click.option("--token", required=True, help="Client token on remote side")
def stats_push(client_uuid, token):
    """Push stats for the local client specified in parameter to an other stats
    server.
    """
    client = Client.query.filter(Client.uuid == client_uuid).first()

    headers = {"X-API-KEY": token, "content-type": "application/json"}

    payload = []
    stats = Stats.query.filter(Stats.client_id == client.id)
    for stat in stats:
        payload.append(
            {
                "uuid": str(stat.uuid),
                "anr": str(stat.anr),
                "type": stat.type,
                "date": str(stat.date),
                "data": stat.data,
            }
        )

    try:
        print("Pushing stats for client {}".format(client.name))
        r = requests.post(STATS_API_ENDPOINT, data=json.dumps(payload), headers=headers)
        if r.status_code not in [200, 204]:
            print("Impossible to push some stats.")
        print(json.loads(r.content))
    except Exception as e:
        print(e)


@application.cli.command("stats_pull")
@click.option("--client-uuid", default="", help="Local client uuid")
@click.option("--token", required=True, help="Client token on remote side")
@click.option(
    "--stats-type",
    required=True,
    help="Type of the stats to import (risk, vulnerability, threat).",
)
def stats_pull(client_uuid, token, stats_type):
    """Pull stats from an other stats instance for the local client specified
    in parameter.
    """
    client = Client.query.filter(Client.uuid == client_uuid).first()

    headers = {"X-API-KEY": token}
    payload = {"type": stats_type}

    r = requests.get(STATS_API_ENDPOINT, params=payload, headers=headers)
    stats = json.loads(r.content)
    for stat in stats["data"]:
        try:
            new_stat = Stats(**stat, client_id=client.id)
            db.session.add(new_stat)
            db.session.commit()
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError) as e:
            logger.error("Duplicate stats {}".format(stat["uuid"]))
            db.session.rollback()
