#! /usr/bin/env python
import logging

import flask_principal
from flask_login import current_user
from flask_restx import abort
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from statsservice.api.v1.common import auth_func
from statsservice.api.v1.common import check_client_user_agent
from statsservice.api.v1.common import clients_params_model
from statsservice.api.v1.identity import admin_permission
from statsservice.bootstrap import application
from statsservice.bootstrap import db
from statsservice.models import Client


logger = logging.getLogger(__name__)

client_ns = Namespace("client", description="client related operations")

# Response marshalling
clients = client_ns.model("Clients", clients_params_model)


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument(
    "name",
    type=str,
    help="The name of the client to create.",
    required=True,
    location="json",
)
parser.add_argument(
    "is_sharing_enabled",
    type=bool,
    help="Specify if the sharing of data is enabled.",
    required=True,
    location="json",
)
parser.add_argument(
    "token",
    type=str,
    help="The token of the client to create.",
    required=True,
    location="json",
)


@client_ns.route("/")
class ClientsList(Resource):
    """Create new clients."""

    method_decorators = [check_client_user_agent]

    @client_ns.doc("client_create")
    @client_ns.expect(parser)
    @client_ns.marshal_with(clients, code=201)
    @auth_func
    def post(self):
        """Create a new client."""
        args = parser.parse_args(strict=True)
        try:
            with admin_permission.require():
                if application.config.get("CLIENT_REGISTRATION_OPEN", True):
                    new_client = Client(
                        name=args.get("name"),
                        is_sharing_enabled=args.get("is_sharing_enabled"),
                        token=args.get("token"),
                    )
                    db.session.add(new_client)
                    db.session.commit()
                else:
                    return {}, 204
        except flask_principal.PermissionDenied:
            logger.error("Only admin can create new client.")
            abort(403)

        return new_client, 201


@client_ns.route("/me")
class GetClient(Resource):
    """Get client details."""

    method_decorators = [check_client_user_agent]

    @client_ns.doc("client_get")
    @client_ns.marshal_with(clients, code=200)
    @auth_func
    def get(self):
        return current_user, 200

    # @client_ns.doc("client_patch")
    # @client_ns.expect(parser)
    # @client_ns.marshal_with(clients, code=201)
    # @auth_func
    # def patch(self):
    #     args = parser.parse_args(strict=True)
    #     if current_user.is_sharing_enabled != args.get("is_sharing_enabled"):
    #         try:
    #             current_user.is_sharing_enabled = args.get("is_sharing_enabled")
    #             db.session.commit()
    #         except Exception:
    #             logger.error("Client patch error.")
    #             return current_user, 500
    #
    #     return current_user, 201
