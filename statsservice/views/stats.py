#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, abort

import statsservice.lib.processors
from statsservice.models import Stats


# stats_bp: blueprint for public only routes which returns different kind of statistics
stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")

# Do not use query filters on Client or on ANR here. It would be in
# contradiction with the finality of this blueprint.


@stats_bp.route("/", methods=["GET"])
def stats():
    """The only view of this blueprint which is supposed to return a HTML file.
    Routes defined in the following can be used in this HTML file.
    """
    return render_template("stats.html")


@stats_bp.route("/threats.json", methods=["GET"])
def threats():
    """Returns threats with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="threat_average_on_date", type=str
    )
    query = Stats.query.filter(
        Stats.type == "threat", Stats.date >= now - timedelta(days=nb_days)
    )
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description="There is no such processor: '{}'.".format(processor),
        )

    return jsonify(result)


@stats_bp.route("/risks.json", methods=["GET"])
def risks():
    """Returns risks with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="threat_average_on_date", type=str
    )
    query = Stats.query.filter(
        Stats.type == "risk", Stats.date >= now - timedelta(days=nb_days)
    )
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description="There is no such processor: '{}'.".format(processor),
        )

    return jsonify(result)


@stats_bp.route("/vulnerabilities.json", methods=["GET"])
def vulnerabilities():
    """Returns vulnerabilities with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="vulnerability_average_on_date", type=str
    )
    query = Stats.query.filter(
        Stats.type == "vulnerability", Stats.date >= now - timedelta(days=nb_days)
    )
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description="There is no such processor: '{}'.".format(processor),
        )

    return jsonify(result)
