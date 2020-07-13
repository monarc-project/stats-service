#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_restx.inputs import date_from_iso8601
from datetime import date
from dateutil.relativedelta import relativedelta

from statsservice.bootstrap import db
from statsservice.models import Stats, Client
from statsservice.api.v1.common import auth_func, uuid_type
from statsservice.lib.processors import aggregate_risks, groups_threats
from statsservice.lib.stats import average_threats

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
    help="The date of the stats must be bigger or equal than this value.",
)
parser.add_argument(
    "date_to",
    type=date_from_iso8601,
    help="The date of the stats must be smaller or equal than this value.",
)
parser.add_argument("page", type=int, required=False, default=1, help="Page number")
parser.add_argument("per_page", type=int, required=False, default=10, help="Page size")


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

        args = parser.parse_args()
        offset = args.pop("page", 1) - 1
        limit = args.pop("per_page", 10)

        date_from = args.pop(
            "date_from",
            (date.today() + relativedelta(months=-3)).strftime('%Y-%m-%d')
        )
        date_to = args.pop(
            "date_to",
            date.today().strftime("%Y-%m-%d"))
        )
        type = args.pop("type")

        result = {
            "data": [],
            "metadata": {"count": 0, "offset": offset, "limit": limit},
        }

        try:
            query = Stats.query.filter(
                Stats.type = type,
                Stats.date >= date_from,
                Stats.date <= date_to,
            )

            # TODO: perform aggregation of the results if needed.
            # TODO: group by anr always by default, will see later for BO, if there should be a separate param.
#             if args.get("type", "") == "threat":
#                 groups = groups_threats(results)
#                 average_threats(results)


            # Count the result, then paginate
            count = query.count()
            query = query.limit(limit)
            results = query.offset(offset * limit)
        except Exception as e:
            print(e)

        result["data"] = results
        result["metadata"]["count"] = count

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
