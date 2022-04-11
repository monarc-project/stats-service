#! /usr/bin/env python
import os
import subprocess
import sys

from flask import Blueprint
from flask import jsonify
from flask_login import login_required

from statsservice.bootstrap import application
from statsservice.views.common import admin_permission


# stats_bp: blueprint for
admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


@admin_bp.before_request
@login_required
@admin_permission.require(http_exception=403)
def restrict_bp_to_admins():
    """Decorator to restrict the blueprint to users with admin permissions."""
    pass


@admin_bp.route("/client_sharing_activate.json/<uuid:client_uuid>", methods=["GET"])
def client_sharing_activate(client_uuid):
    """Enable the sharing of stats for a client."""
    env = os.environ.copy()
    env["FLASK_APP"] = "runserver.py"
    cmd = [
        sys.exec_prefix + "/bin/flask",
        "client_sharing_activate",
        "--uuid",
        str(client_uuid),
    ]

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )
    stdout, stderr = process.communicate()
    if stderr:
        result = "KO"
        http_code = 400
    else:
        result = "OK"
        http_code = 200

    return jsonify({"result": result, "stderr": str(stderr)}), http_code


@admin_bp.route("/client_sharing_deactivate.json/<uuid:client_uuid>", methods=["GET"])
def client_sharing_deactivate(client_uuid):
    """Disable the sharing of stats for a client."""
    env = os.environ.copy()
    env["FLASK_APP"] = "runserver.py"
    cmd = [
        sys.exec_prefix + "/bin/flask",
        "client_sharing_deactivate",
        "--uuid",
        str(client_uuid),
    ]

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )
    stdout, stderr = process.communicate()
    if stderr:
        result = "KO"
        http_code = 400
    else:
        result = "OK"
        http_code = 200

    return jsonify({"result": result, "stderr": str(stderr)}), http_code


@admin_bp.route("/update.json", methods=["GET"])
def update():
    """Trigger the update of Stats Service with the shell script: ./contrib/update.sh."""
    root_path = os.path.dirname(application.instance_path)
    process = subprocess.Popen(
        ["./contrib/update.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=root_path,
    )
    process.wait()
    content = ""
    if process.stdout:
        for line in process.stdout.readlines():
            print(line)
            content += str(line)
    return jsonify({"result": "OK", "stdout": content})
