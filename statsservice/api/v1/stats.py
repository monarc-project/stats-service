#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_restx.inputs import date_from_iso8601
from datetime import date
from dateutil.relativedelta import relativedelta

import statsservice.lib.processors
from statsservice.bootstrap import db
from statsservice.models import Stats, Client
from statsservice.api.v1.common import auth_func, uuid_type



stats_ns = Namespace("stats", description="stats related operations")


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("anr", type=uuid_type, help="The ANR UUID related to this stats.")
parser.add_argument(
    "type",
    type=str,
    help="The type of the stats.",
    required=True,
    choices=("risk", "vulnerability", "threat", "cartography", "compliance"),
)
parser.add_argument(
    "aggregation_period",
    type=str,
    help="The period of the stats aggregation.",
    required=False,
    choices=("day", "week", "month", "quarter", "year"),
)
parser.add_argument(
    "date_from",
    type=date_from_iso8601,
    required=False,
    help="The date of the stats must be bigger or equal than this value.",
)
parser.add_argument(
    "date_to",
    type=date_from_iso8601,
    required=False,
    help="The date of the stats must be smaller or equal than this value.",
)
parser.add_argument("offset", type=int, required=False, default=0, help="Start position")
parser.add_argument("limit", type=int, required=False, default=0, help="Limit of records")


# Response marshalling
stats = stats_ns.model(
    "Stats",
    {
        "uuid": fields.String(readonly=True, description="The stats unique identifier"),
        "anr": fields.String(description="The ANR UUID related to this stats."),
        "type": fields.String(
            description="The type of this stats (risk, vulnerability, threat, cartography or compliance)."
        ),
        "date": fields.Raw(description="The stats date in format 'Y-m-d'"),
        "data": fields.Raw(description="The stats as a dynamic JSON object."),
    },
)

metadata = stats_ns.model(
    "metadata",
    {
        "count": fields.String(
            readonly=True, description="Total number of the items of the data."
        ),
        "offset": fields.String(
            readonly=True,
            description="Position of the first element of the data from the total data amount.",
        ),
        "limit": fields.String(readonly=True, description="Requested limit data."),
    },
)

stats_list_fields = stats_ns.model(
    "StatsList",
    {
        "metadata": fields.Nested(
            metadata, description="Metada related to the result."
        ),
        "data": fields.List(fields.Nested(stats), description="List of stats objects."),
    },
)


@stats_ns.route("/")
class StatsList(Resource):
    """Shows a list of all the stats, and lets you POST to add new stats"""

    @stats_ns.doc("list_stats")
    @stats_ns.expect(parser)
    @stats_ns.marshal_list_with(stats_list_fields)
    @stats_ns.response(401, "Authorization needed")
    @auth_func
    def get(self):
        """List all stats"""
        # get the client token
        token = request.headers.get("X-API-KEY", False)
        client = Client.query.filter(Client.token == token).first()

        args = parser.parse_args(strict=True)
        limit = args.get("limit", 0)
        offset = args.get("offset", 0)
        type = args.get("type")
        aggregation_period = args.get("aggregation_period")
        date_from = args.get("date_from")
        date_to = args.get("date_to")
        if date_from is None:
            date_from = (date.today() + relativedelta(months=-3)).strftime('%Y-%m-%d')
        if date_to is None:
            date_to = date.today().strftime("%Y-%m-%d")

        result = {
            "data": [],
            "metadata": {"count": 0, "offset": offset, "limit": limit},
        }

        try:
            query = Stats.query.filter(
                Stats.type == type,
                Stats.date >= date_from,
                Stats.date <= date_to,
            )

            if aggregation_period is None and limit > 0:
                query = query.limit(limit)
                results = query.offset(offset)
            else:
                results = query.all()
                # TODO: 1. we go for the aggregation here in case if aggregation_period is set and then apply the limit if limit > 0.

                try:
                    getattr(statsservice.lib.processors, 'process_'+type)(results)
                except AttributeError as e:
                    print('No process defined for the type.')

        except Exception as e:
            print(e)

        result["data"] = results
        # We count already aggregated results, if they are aggregated.
        result["metadata"]["count"] = len(results)

        return result, 200

    @stats_ns.doc("create_stats")
    @stats_ns.expect([stats])
    @stats_ns.marshal_with(stats, code=201)
    @auth_func
    def post(self):
        """Create a new stats"""
        # set the appropriate client thanks to the token
        token = request.headers.get("X-API-KEY", False)
        client = Client.query.filter(Client.token == token).first()
        # create the new stats
        news_stats = []
        for stats in stats_ns.payload:
            news_stats.append(Stats(**stats, client_id=client.id))
        db.session.bulk_save_objects(news_stats)
        db.session.commit()
        return {}, 204


@stats_ns.route("/<string:uuid>")
@stats_ns.response(404, "Stats not found")
@stats_ns.param("uuid", "The stats identifier")
class StatsItem(Resource):
    """Show a single stats item and lets you delete them"""

    @stats_ns.doc("get_stats")
    @stats_ns.marshal_with(stats)
    @auth_func
    def get(self, uuid):
        """Fetch a given resource"""
        return Stats.query.filter(Stats.uuid == uuid).first(), 200

    @stats_ns.doc("delete_stats")
    @stats_ns.response(204, "Stats deleted")
    @auth_func
    def delete(self, uuid):
        """Delete a stats given its identifier"""
        # TODO: check permissions
        try:
            Stats.objects(anr__exact=uuid).delete()
            return "", 204
        except:
            abort(404, Error="Impossible to delete the stats.")

    @stats_ns.expect(stats)
    @stats_ns.marshal_with(stats)
    @auth_func
    def put(self, uuid):
        """Update a stats given its identifier"""
        # return Stats.objects(uuid__exact=uuid).update(**stats_ns.payload)
        pass
