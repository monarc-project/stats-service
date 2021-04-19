#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request
from flask_restx import Namespace, Resource, fields, abort
from flask_login import current_user

from statsservice.bootstrap import db
from statsservice.models import Client
from statsservice.api.v1.common import (
    auth_func,
    clients_params_model,
    check_client_user_agent,
)
from statsservice.api.v1.identity import admin_permission


logger = logging.getLogger(__name__)

client_ns = Namespace("client", description="client related operations")

# Response marshalling
clients = client_ns.model("Clients", clients_params_model)


@client_ns.route("/")
class ClientsList(Resource):
    """Create new clients."""

    method_decorators = [check_client_user_agent]

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

    method_decorators = [check_client_user_agent]

    @client_ns.doc("client_get")
    @client_ns.marshal_with(clients, code=200)
    @auth_func
    def get(self):
        return current_user, 200

    @client_ns.doc("client_patch")
    @client_ns.expect(clients)
    @client_ns.marshal_with(clients, code=201)
    @auth_func
    def patch(self):
        if current_user.is_sharing_enabled != client_ns.payload["is_sharing_enabled"]:
            try:
                current_user.is_sharing_enabled = client_ns.payload[
                    "is_sharing_enabled"
                ]
                db.session.commit()
            except:
                logger.error("Client patch error.")
                return current_user, 500

        return current_user, 201
