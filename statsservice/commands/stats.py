import json
import logging
import click
import requests
import sqlalchemy.exc

from datetime import date
from dateutil.relativedelta import relativedelta
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


@application.cli.command("stats_purge")
@click.option("--nb-month", default=36, help="Age (in months) of the stats to purge.")
def stats_purge(nb_month):
    """Delete the stats older than the number of months specified in parameter."""
    print("Deleting stats older than {} months...".format(nb_month))
    date_to = (date.today() - relativedelta(months=nb_month)).strftime("%Y-%m-%d")
    # query = Stats.query.filter(Stats.date <= date_to)
    try:
        Stats.query.filter(Stats.date <= date_to).delete()
        db.session.commit()
    except Exception as e:
        print(e)


@application.cli.command("stats_remove_duplicate")
@click.option(
    "--client-uuid", default="", help="UUID of the lclient related to the stats."
)
def stats_remove_duplicate(client_uuid):
    """Delete the stats older than the number of months specified in parameter."""
    print("Deleting duplicate stats for {}...".format(client_uuid))
    # query = Stats.query.filter(Stats.date <= date_to)
    try:
        Stats.query.filter(Stats.client.has(uuid=client_uuid))  # .delete()
        db.session.commit()
    except Exception as e:
        print(e)


@application.cli.command("stats_push")
@click.option(
    "--date-from",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today() + relativedelta(months=-3)),
    help="Only stats more recent than this date will be pushed. Default value is 3 months before today.",
)
@click.option(
    "--date-to",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Only stats older than this date will be pushed. Default value is today.",
)
def stats_push(date_from, date_to):
    """Pushes the clients stats to the global stats server."""

    if date_from > date_to:
        print("Error: --date-from option must be before --date-to.")

    headers = {
        "X-API-KEY": application.config["REMOTE_STATS_TOKEN"],
        "content-type": "application/json",
    }
    payload = []

    clients = Client.query.filter(Client.is_sharing_enabled == True)
    for client in clients:
        stats = Stats.query.filter(
            Stats.client_id == client.id, Stats.date >= date_from, Stats.date <= date_to
        )
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
    r = requests.get(STATS_API_ENDPOINT, json=payload, headers=headers)
    stats = json.loads(r.content)
    for stat in stats["data"]:
        try:
            new_stat = Stats(**stat, client_id=client.id)
            db.session.add(new_stat)
            db.session.commit()
        except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError) as e:
            logger.error("Duplicate stats {}".format(stat["uuid"]))
            db.session.rollback()
