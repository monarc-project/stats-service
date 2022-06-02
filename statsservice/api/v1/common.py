#! /usr/bin/env python
import uuid

from flask import request
from flask_restx import abort
from flask_restx import fields
from packaging import version

from statsservice.api.v1.identity import login_user_bundle
from statsservice.models import Client


def uuid_type(value):
    """Parse UUID"""
    try:
        val = uuid.UUID(value)
    except ValueError:
        raise ValueError("This is not a valid UUID.")
    return val


# Swagger documentation
setattr(uuid_type, "__schema__", {"type": "string", "format": "uuid_type"})  # noqa


def auth_func(func):
    def wrapper(*args, **kwargs):
        if "X-API-KEY" in request.headers:
            token = request.headers.get("X-API-KEY", False)
            if token:
                client = Client.query.filter(Client.token == token).first()
                login_user_bundle(client)
                if not client:
                    abort(403, Error="Forbidden - Authentication failed.")
        else:
            abort(401, Error="Unauthorized - Authentication required.")
        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper


def check_client_user_agent(meth):
    """Check the User-Agent sent by a MONARC client."""
    user_agent = request.headers.get("User-Agent", "")

    if "MONARC/" in user_agent:
        try:
            monarc_version = user_agent.split("/")[1]
        except Exception:
            # failed to extract the version of MONARC, cancels the check
            return meth
        if version.parse(monarc_version) < version.parse("2.10.2"):
            abort(426, Error="This service requires use of MONARC version >= 2.10.2.")

    return meth


# Params for models marshalling

metada_params_model = {
    "count": fields.String(
        readonly=True, description="Total number of the items of the data."
    ),
    "offset": fields.String(
        readonly=True,
        description="Position of the first element of the data from the total data amount.",
    ),
    "limit": fields.String(readonly=True, description="Requested limit data."),
}

stats_params_model = {
    "uuid": fields.String(readonly=True, description="The stats unique identifier"),
    "anr": fields.String(description="The ANR UUID related to this stats."),
    "type": fields.String(
        description="The type of this stats (risk, vulnerability, threat, cartography or compliance)."
    ),
    "date": fields.Date(description="The stats date in format 'Y-m-d'"),
    "data": fields.Raw(description="The stats as a dynamic JSON object."),
}

clients_params_model = {
    "name": fields.String(description="The client name."),
    "token": fields.String(readonly=True, description="The token of the client."),
    "role": fields.String(readonly=True, description="The client role."),
    "is_sharing_enabled": fields.Boolean(
        description="If the statistics sharing is enabled or not."
    ),
}
