#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify, abort

from statsservice.models import Client


# stats_bp: blueprint for public only routes which returns different kind of statistics
map_bp = Blueprint("map_bp", __name__, url_prefix="/map")


@map_bp.route("/", methods=["GET"])
def index():
    return render_template("map.html")


@map_bp.route("/clients.json", methods=["GET"])
def clients():
    clients = Client.query.filter().all()

    result = []

    for client in clients:
        result.append({
            "latitude": client.latitude,
            "longitude": client.longitude,
        })

    return jsonify(result)
