#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, abort

import statsservice.lib.postprocessors
from statsservice.models import Stats


# stats_bp: blueprint for public only routes which returns different kind of statistics
stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")


@stats_bp.route("/", methods=["GET"])
def stats():
    """The only view of this blueprint which is supposed to return a HTML file.
    Routes defined in the following can be used in this HTML file.
    """
    return render_template("stats.html")


@stats_bp.route("/risks.json", methods=["GET"])
def risks():
    """
    Returns risks as JSON.
    """
    # risks = Stats.objects(**{'{}__{}'.format(field, operator): 18})
    # risks = Stats.objects(data__anr__exact=2)
    query = Stats.query.filter(Stats.type == "risk")
    result = getattr(statsservice.lib.postprocessors, "risk_process")(query.all())
    return jsonify(result)  # result.to_json()


@stats_bp.route("/threats.json", methods=["GET"])
def threats():
    """Returns threats with custom post-processings.
    """
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    postprocessor = request.args.get(
        "postprocessor", default="threat_average_on_date", type=str
    )
    query = Stats.query.filter(
        Stats.type == "threat", Stats.date >= now - timedelta(days=nb_days)
    )

    try:
        result = getattr(statsservice.lib.postprocessors, postprocessor)(query.all())
    except AttributeError:
        abort(
            500,
            description="There is no such postprocessor: '{}'.".format(postprocessor),
        )

    return jsonify(result)


@stats_bp.route("/vulnerabilities.json", methods=["GET"])
def vulnerabilities():
    """Returns vulnerabilities with custom post-processings.
    """
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    postprocessor = request.args.get(
        "postprocessor", default="vulnerability_average_on_date", type=str
    )
    query = Stats.query.filter(
        Stats.type == "vulnerability", Stats.date >= now - timedelta(days=nb_days)
    )

    try:
        result = getattr(statsservice.lib.postprocessors, postprocessor)(query.all())
    except AttributeError:
        abort(
            500,
            description="There is no such postprocessor: '{}'.".format(postprocessor),
        )

    return jsonify(result)
