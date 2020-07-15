#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_user import roles_required

from statsservice.bootstrap import db
from statsservice.models import Client
from statsservice.api.v1.common import auth_func

client_ns = Namespace(
    "client", description="client related operations"
)

# Response marshalling
clients = client_ns.model(
    "Clients",
    {
        "name": fields.String(description="The client name."),
        "token": fields.String(
            readonly=True, description="The token of the client."
        ),
        "role": field.string(readonly=True, description="The client role.")
    },
)


@client_ns.route("/")
class ClientsList(Resource):
    """Create new clients."""

    @client_ns.doc("create_client")
    @client_ns.expect(clients)
    @client_ns.marshal_with(clients, code=201)
    @roles_required(Client.ROLE_ADMIN)
    def post(self):
        """Create a new client."""
        new_client = Client(**client_ns.payload)
        db.session.add(new_client)
        db.session.commit()
        return new_client, 201
