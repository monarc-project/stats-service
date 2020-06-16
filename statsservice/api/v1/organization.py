#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse, abort

from statsservice.bootstrap import db
from statsservice.models import Organization
from statsservice.api.v1.common import auth_func


organization_ns = Namespace(
    "organization", description="organization related operations"
)


# Response marshalling
orgs = organization_ns.model(
    "Orgs",
    {
        "name": fields.String(description="The organization name."),
        "token": fields.String(
            readonly=True, description="The token of the organization."
        ),
    },
)


@organization_ns.route("/")
class OrganizationsList(Resource):
    """Create new organizations."""

    @organization_ns.doc("create_organization")
    @organization_ns.expect(orgs)
    @organization_ns.marshal_with(orgs, code=201)
    def post(self):
        """Create a new organization."""
        new_organization = Organization(**organization_ns.payload)
        db.session.add(new_organization)
        db.session.commit()
        return new_organization, 201
