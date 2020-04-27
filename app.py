#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods
from flask_mongorest.authentication import AuthenticationBase


application = Flask(__name__)

application.config.update(
    MONGODB_HOST="localhost", MONGODB_PORT=27017, MONGODB_DB="stats_api_dev",
)

db = MongoEngine(application)
api = MongoRest(application)

#
# Documents
#
class Organization(db.Document):
    token = db.DynamicField(unique=True, required=True)


# class Data(db.EmbeddedDocument):
#     json = db.DynamicField()


class Stats(db.Document):
    organization = db.ReferenceField(Organization)
    type = db.StringField(max_length=120, required=True)
    day = db.IntField(required=True)
    week = db.IntField(required=True)
    month = db.IntField(required=True)
    data = db.DynamicField()  # db.EmbeddedDocumentField(Data)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)


#
# Authentication
#

class ApiKeyAuthentication(AuthenticationBase):
    """Custom token based authentication. To be inproved."""
    def authorized(self):
        if 'AUTHORIZATION' in request.headers:
            authorization = request.headers['AUTHORIZATION'].split()
            if len(authorization) == 2 and authorization[0].lower() == 'basic':
                try:
                    token = authorization[1]
                    token_key = Organization.objects.get(token__exact=token)
                    print(token_key)
                    # if token_key.user:
                    #     login_user(token_key.user)
                    #     setattr(current_user, 'token_key', token_key)
                    return True
                except (TypeError, UnicodeDecodeError, Organization.DoesNotExist):
                    pass
        return False


#
# Resources
#

# Stats
class StatsResource(Resource):
    document = Stats
    filters = {
        'type': [ops.Exact, ops.IExact, ops.Contains, ops.IContains],
        'organization': [ops.Exact],
        'created_at': [ops.Exact, ops.IExact, ops.Contains, ops.IContains],
    }
    # fields = ['type']
    # filters = {"created_at": [ops.Exact]}
    paginate = True
    default_limit = 100
    max_limit = 100
    bulk_update_limit = 100


@api.register()
class StatsView(ResourceView):
    resource = StatsResource
    methods = [
        methods.Create,
        methods.Update,
        methods.Fetch,
        methods.List,
        methods.Delete,
    ]
    authentication_methods = [ApiKeyAuthentication]


# Organization
class OrganizationResource(Resource):
    document = Organization


@api.register()
class OrganizationView(ResourceView):
    resource = OrganizationResource
    methods = [
        methods.Create,
        methods.Update,
        methods.Fetch,
        methods.List,
        methods.Delete,
    ]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port)
