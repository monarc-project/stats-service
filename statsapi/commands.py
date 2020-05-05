#! /usr/bin/env python
# -*- coding: utf-8 -*-

import click

from statsapi.bootstrap import application, db
from statsapi.documents import Stats, Organization


@application.cli.command("push-stats")
@click.option('--uuid', default='', help='Organization UUID')
def push_stats(uuid):
    "Push stats."
    organization = Organization.objects.get(id__exact=uuid)
    stats = Stats.objects(organization__exact=organization)
    for stat in stats:
        print("{} {}".format(stat.created_at, stat.type))
