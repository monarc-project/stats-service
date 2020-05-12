#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import requests

from urllib.parse import urljoin
from statsapi.bootstrap import application, db
from statsapi.documents import Stats, Organization

STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("push-stats")
@click.option("--name", default="", help="Organization name")
def push_stats(name):
    """Push stats for the organization specified in parameter to an other stats
    server.
    """
    organization = Organization.objects.get(name__exact=name)
    stats = Stats.objects(organization__exact=organization)
    for stat in stats:
        print("Pushing stats {} {}".format(stat.created_at, stat.type))

        # payload = stat.to_json()
        payload = json.dumps(
            {
                "uuid": str(stat.uuid),
                "organization": name,
                "type": stat.type,
                "data": stat.data,
                "day": stat.day,
                "week": stat.week,
                "month": stat.month,
            }
        )

        r = requests.post(STATS_API_ENDPOINT, data=payload)

        if r.status_code != 200:
            print("Impossible to push the stat.")
