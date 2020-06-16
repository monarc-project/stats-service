#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import requests

from urllib.parse import urljoin
from statsservice.bootstrap import application, db
from statsservice.models import Stats, Organization

STATS_API_ENDPOINT = urljoin(
    application.config["REMOTE_STATS_SERVER"], "/api/v1/stats/"
)


@application.cli.command("push-stats")
@click.option("--name", default="", help="Organization name")
@click.option("--token", default="", help="Organization token on remote side")
def push_stats(name, token):
    """Push stats for the organization specified in parameter to an other stats
    server.
    """
    organization = Organization.objects.get(name__exact=name)

    headers = {"X-API-KEY": token, "content-type": "application/json"}

    stats = Stats.objects(organization__exact=organization)
    for stat in stats:
        print("Pushing stats {} {}".format(stat.created_at, stat.type))

        # payload = stat.to_json()
        payload = json.dumps(
            {
                "uuid": str(stat.uuid),
                "anr": str(stat.anr),
                "type": stat.type,
                "day": stat.day,
                "week": stat.week,
                "month": stat.month,
                "quarter": stat.month,
                "year": stat.year,
                "data": stat.data,
            }
        )

        try:
            r = requests.post(STATS_API_ENDPOINT, data=payload, headers=headers)
            if r.status_code != 200:
                print("Impossible to push the stat.")
        except:
            pass
