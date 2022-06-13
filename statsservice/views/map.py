#! /usr/bin/env python
import operator

from flask import Blueprint
from flask import jsonify
from flask import render_template

import statsservice.lib.processors
from statsservice.models import Client
from statsservice.models import Stats


# stats_bp: blueprint for public only routes which returns different kind of statistics
map_bp = Blueprint("map_bp", __name__, url_prefix="/map")


@map_bp.route("/", methods=["GET"])
def index():
    return render_template("map.html")


@map_bp.route("/clients.json", methods=["GET"])
def clients():
    clients = Client.query.filter(
        Client.latitude != None, Client.longitude != None  # noqa
    ).all()

    result = []

    for client in clients:
        query = Stats.query.filter(Stats.type == "threat", Stats.client_id == client.id)
        query = query.order_by(Stats.date.desc()).limit(40)
        if not query.count():
            continue
        threats = getattr(  # noqa
            statsservice.lib.processors, "threat_average_on_date"
        )(query.all())
        try:
            max_threat = max(
                ((threat["averages"]["count"], threat["object"]) for threat in threats),
                key=operator.itemgetter(0),
            )
        except ValueError:
            # ValueError: max() arg is an empty sequence
            max_threat = ("", "")

        query = Stats.query.filter(
            Stats.type == "vulnerability", Stats.client_id == client.id
        )
        query = query.order_by(Stats.date.desc()).limit(40)
        if not query.count():
            continue
        vulnerabilities = getattr(  # noqa
            statsservice.lib.processors, "vulnerability_average_on_date"
        )(query.all())
        try:
            max_vulnerability = max(
                (
                    (vulnerability["averages"]["count"], vulnerability["object"])
                    for vulnerability in vulnerabilities
                ),
                key=operator.itemgetter(0),
            )
        except ValueError:
            # ValueError: max() arg is an empty sequence
            max_vulnerability = ("", "")

        result.append(
            {
                "latitude": client.latitude,
                "longitude": client.longitude,
                "max_threat": max_threat,
                "max_vulnerability": max_vulnerability,
            }
        )

    return jsonify(result)
