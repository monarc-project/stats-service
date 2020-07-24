#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import requests

from urllib.parse import urljoin
from statsservice.bootstrap import application, db
from statsservice.models import Stats, Client

STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("push-stats")
@click.option("--name", default="", help="Client name")
@click.option("--token", default="", help="Client token on remote side")
def push_stats(name, token):
    """Push stats for the client specified in parameter to an other stats
    server.
    """
    client = Client.objects.get(name__exact=name)

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
