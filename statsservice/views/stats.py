#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify

from statsservice.models import Stats
from statsservice.lib.utils import groups_threats
from statsservice.lib.processors import process_threat, process_risk, threats_average_on_date


# stats_bp: blueprint for public only routes which returns different kind of statistics
stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")


@stats_bp.route('/', methods=['GET'])
def stats():
    """The only view of this blueprint which is supposed to return a HTML file.
    Routes defined in the following can be used in this HTML file.
    """
    return render_template('stats.html')


@stats_bp.route("/risks.json", methods=["GET"])
def risks():
    """
    Returns risks as JSON.
    """
    # risks = Stats.objects(**{'{}__{}'.format(field, operator): 18})
    # risks = Stats.objects(data__anr__exact=2)
    query = Stats.query.filter(Stats.type == "risk")
    result = process_risk(query.all())
    return jsonify(result)  # result.to_json()


@stats_bp.route("/threats.json", methods=["GET"])
def threats():
    """Returns threats with custom post-processings.
    """
    now = datetime.today()
    nb_days = request.args.get("days", default=365, type=int)
    format_result = request.args.get("format", default="mean", type=str)
    query = Stats.query.filter(
        Stats.type == "threat", Stats.date >= now - timedelta(days=nb_days)
    )

    if format_result == "aggregated":
        result = groups_threats(query.all())
    elif format_result == "mean":
        result = process_threat(query.all())
    elif format_result == "average_date":
        result = threats_average_on_date(query.all())
    else:
        result = {"error": "Format '{}' not recognized.".format(format_result)}

    return jsonify(result)
