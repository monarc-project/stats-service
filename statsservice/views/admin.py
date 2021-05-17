#! /usr/bin/env python
# -*- coding: utf-8 -*-

import operator
from flask import Blueprint, render_template, request, jsonify, abort

import statsservice.lib.processors
from statsservice.models import Client, Stats


# stats_bp: blueprint for
admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


@admin_bp.route("/client_sharing_activate.json/<client_uuid>", methods=["GET"])
def client_sharing_activate(client_uuid):

    env = os.environ.copy()
    env['FLASK_APP'] = 'runserver.py'
    cmd = [
        sys.exec_prefix + "/bin/flask",
        "client_sharing_activate",
        "--uuid", str(client_uuid),
    ]

    subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)

    return jsonify({"result": "OK"})
