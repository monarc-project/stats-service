import json
import logging
from datetime import date
from itertools import groupby
from operator import attrgetter
from typing import Any
from typing import Dict
from typing import Optional
from urllib.parse import urljoin

import click
import requests
import sqlalchemy.exc
from dateutil.relativedelta import relativedelta

from statsservice.bootstrap import application
from statsservice.bootstrap import db
from statsservice.lib.utils import dict_hash
from statsservice.models import Client
from statsservice.models import Stats


logger = logging.getLogger(__name__)


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
    print(f"Deleting stats older than {nb_month} months...")
    date_to = (date.today() - relativedelta(months=nb_month)).strftime("%Y-%m-%d")
    # query = Stats.query.filter(Stats.date <= date_to)
    try:
        Stats.query.filter(Stats.date <= date_to).delete()
        db.session.commit()
    except Exception as e:
        print(e)


@application.cli.command("stats_remove_duplicate")
@click.option(
    "--type", required=True, help="Type of the stats (vulnerability, threat or risk)."
)
@click.option("--nb-month", default=0, help="Minimum age (in months) of the stats.")
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically reply yes to the deletion confirmation message.",
)
def stats_remove_duplicate(type, nb_month, yes) -> None:
    """Delete duplicate stats that are older than the number of months specified in
    parameter."""
    to_delete = []

    query = db.session.query(Stats.anr).filter(Stats.type == type)

    if nb_month:
        date_to = (date.today() - relativedelta(months=nb_month)).strftime("%Y-%m-%d")
        query = query.filter(Stats.date <= date_to)

    print("Searching for duplicate stats...")
    query = query.with_entities(
        Stats.anr, Stats.uuid, Stats.type, Stats.data, Stats.date
    ).order_by(Stats.anr)

    elems = query.all()
    elems_per_anr = [list(g) for k, g in groupby(elems, attrgetter("anr"))]

    for elems in elems_per_anr:
        previous_date: Optional[date] = None
        previous_data: Optional[Dict[str, Any]] = None
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

    if yes or click.confirm(f"Do you want to delete {len(to_delete)} duplicate stats?"):
        print("Removing the duplicate stats...")
        try:
            deleted_objects = Stats.__table__.delete().where(Stats.uuid.in_(to_delete))
            db.session.execute(deleted_objects)
            db.session.commit()
        except Exception as e:
            print(e)


@application.cli.command("stats_push")
@click.option(
    "--local-client-uuid", default="", help="UUID of the client related to the stats."
)
@click.option("--remote-token", default="", help="Client token on remote side.")
@click.option(
    "--date-from",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today() + relativedelta(months=-3)),
    help="Only stats more recent than this date will be pushed. Default value is 1 month before the current day.",
)
@click.option(
    "--date-to",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Only stats older than this date will be pushed. Default value is today.",
)
def stats_push(local_client_uuid, remote_token, date_from, date_to):
    """Pushes the clients stats to the global stats server.

    Only the stats of the clients with the flag `is_sharing_enabled` set to True
    will be pushed.

    If you specify the UUID of a client only the stats of this client will be
    pushed (and if `is_sharing_enabled` is set to True for this client).

    The parameter `remote_token` is used for the authentication to the remote
    stats service and to 'identify' the client on the remote side.
    """

    if date_from > date_to:
        print("Error: --date-from option must be before --date-to.")

    headers = {
        "X-API-KEY": remote_token
        if remote_token
        else application.config.get("REMOTE_STATS_TOKEN", ""),
        "content-type": "application/json",
    }

    if not headers["X-API-KEY"]:
        logger.error("Authentication token not set.")
        return

    payload = []

    clients = Client.query.filter(Client.is_sharing_enabled == True)  # noqa
    if local_client_uuid:
        clients = clients.filter(Client.uuid == local_client_uuid)
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
        print(f"Pushing stats for client {client.name}")
        r = requests.post(STATS_API_ENDPOINT, data=json.dumps(payload), headers=headers)
        if r.status_code not in [200, 204]:
            logger.error(
                "Impossible to push some stats (possible duplicates on remote side)."
            )
            print("Impossible to push some stats (possible duplicates on remote side).")
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
            print(e)
