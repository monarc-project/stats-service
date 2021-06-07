import json
import logging
import click
import requests
import sqlalchemy.exc
from itertools import groupby
from operator import attrgetter
from sqlalchemy import func

from datetime import date
from dateutil.relativedelta import relativedelta
from urllib.parse import urljoin
from statsservice.bootstrap import application, db
from statsservice.models import Stats, Client
from statsservice.lib.utils import dict_hash


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
@click.option("--nb-month", default=0, help="Minimym age (in months) of the stats.")
def stats_remove_duplicate(nb_month):
    """Delete duplicate stats that are older than the number of months specified in parameter."""
    to_delete = []

    query = db.session.query(Stats.anr).filter(Stats.type == "vulnerability")

    if nb_month:
        date_to = (date.today() - relativedelta(months=nb_month)).strftime("%Y-%m-%d")
        query = query.filter((Stats.date <= date_to))

    print("Searching for duplicate stats...")
    query = query.with_entities(
        Stats.anr, Stats.uuid, Stats.type, Stats.data, Stats.date
    ).order_by(Stats.anr)

    elems = query.all()
    elems_per_anr = [list(g) for k, g in groupby(elems, attrgetter("anr"))]

    for elems in elems_per_anr:
        previous_date = None
        previous_data = None
        sorted_elems = sorted(elems, key=lambda x: x[4])
        for *b, data, stat_date in sorted_elems:
            print(b, end=" "), print(stat_date)
            if previous_date:
                if previous_date.month < stat_date.month:
                    previous_date = stat_date
                    continue

                if stat_date == previous_date:
                    print("Duplicate stats for this date and stats type.")
                    to_delete.append(b[1])
                    continue  # no need to check the content (Stats.data)
            previous_date = stat_date

            if previous_data:
                if dict_hash(data) == dict_hash(previous_data):
                    print("same content")
                    to_delete.append(b[1])

            previous_data = data

        print(" ")

    if click.confirm("Do you want to delete {} duplicate stats?".format(len(to_delete))):
        print("Removing the duplicate stats...")
        try:
            deleted_objects = Stats.__table__.delete().where(Stats.uuid.in_(to_delete))
            session.execute(deleted_objects)
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
