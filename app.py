#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods

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
