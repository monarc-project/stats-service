#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import requests

from statsapi.bootstrap import application, db
from statsapi.documents import Stats, Organization


@application.cli.command("push-stats")
@click.option("--uuid", default="", help="Organization UUID")
def push_stats(uuid):
    """Push stats for the organization specified in parameter to an other stats
    server.
    """
    organization = Organization.objects.get(id__exact=uuid)
    stats = Stats.objects(organization__exact=organization)
    for stat in stats:
        print("{} {}".format(stat.created_at, stat.type))

        # payload = stat.to_json()
        payload = json.dumps(
            {
                "organization": uuid,
                "type": stat.type,
                "data": stat.data,
                "day": stat.day,
                "week": stat.week,
                "month": stat.month,
            }
        )

        r = requests.post(application.config["REMOTE_STATS_SERVER"], data=payload)

        print(r.content)
