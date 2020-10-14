#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, abort
from flask_restx import Namespace, Resource, fields, abort
from flask_login import current_user

from statsservice.bootstrap import db
from statsservice.models import Client
from statsservice.api.v1.common import auth_func
from statsservice.api.v1.identity import admin_permission


logger = logging.getLogger(__name__)

client_ns = Namespace("client", description="client related operations")

# Response marshalling
clients = client_ns.model(
    "Clients",
    {
        "name": fields.String(description="The client name."),
        "token": fields.String(readonly=True, description="The token of the client."),
        "role": fields.String(readonly=True, description="The client role."),
    },
)


@client_ns.route("/")
class ClientsList(Resource):
    """Create new clients."""

    @client_ns.doc("client_create")
    @client_ns.expect(clients)
    @client_ns.marshal_with(clients, code=201)
    @auth_func
    def post(self):
        """Create a new client."""
        try:
            with admin_permission.require():
                new_client = Client(**client_ns.payload)
                db.session.add(new_client)
                db.session.commit()
                return new_client, 201
        except Exception:
            logger.error("Only admin can create new client.")
            return abort(403)


@client_ns.route("/me")
class GetClient(Resource):
    """Get client details."""

    @client_ns.doc("client_get")
    @client_ns.marshal_with(clients, code=200)
    @auth_func
    def get(self):

        return current_user, 200
