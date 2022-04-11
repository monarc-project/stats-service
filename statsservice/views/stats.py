#! /usr/bin/env python
from datetime import datetime
from datetime import timedelta

from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

import statsservice.lib.processors
from statsservice.models import Stats


# stats_bp: blueprint for public only routes which returns different kind of statistics
stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")

# Do not use query filters on Client or on ANR here. It would be in
# contradiction with the finality of this blueprint.


@stats_bp.route("/threats.json", methods=["GET"])
def threats():
    """Returns threats with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    last_stats = request.args.get("last_stats", default=0, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="threat_average_on_date", type=str
    )

    query = Stats.query.filter(Stats.type == "threat")
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))
    if last_stats:
        query = query.order_by(Stats.date.desc()).limit(40)
    else:
        query = query.filter(Stats.date >= now - timedelta(days=nb_days))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description=f"There is no such processor: '{processor}'.",
        )

    return jsonify(result)


@stats_bp.route("/risks.json", methods=["GET"])
def risks():
    """Returns risks with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    last_stats = request.args.get("last_stats", default=0, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="threat_average_on_date", type=str
    )

    query = Stats.query.filter(Stats.type == "risk")
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))
    if last_stats:
        query = query.order_by(Stats.date >= now - timedelta(days=40))
    else:
        query = query.filter(Stats.date >= now - timedelta(days=nb_days))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description=f"There is no such processor: '{processor}'.",
        )

    return jsonify(result)


@stats_bp.route("/vulnerabilities.json", methods=["GET"])
def vulnerabilities():
    """Returns vulnerabilities with custom processings."""
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    last_stats = request.args.get("last_stats", default=0, type=int)
    local_stats_only = request.args.get("local_stats_only", default=0, type=int)
    processor = request.args.get(
        "processor", default="vulnerability_average_on_date", type=str
    )

    query = Stats.query.filter(Stats.type == "vulnerability")
    if local_stats_only:
        query = query.filter(Stats.client.has(local=True))
    if last_stats:
        query = query.order_by(Stats.date >= now - timedelta(days=40))
    else:
        query = query.filter(Stats.date >= now - timedelta(days=nb_days))

    try:
        result = getattr(statsservice.lib.processors, processor)(query.all())
    except AttributeError:
        abort(
            500,
            description=f"There is no such processor: '{processor}'.",
        )

    return jsonify(result)
