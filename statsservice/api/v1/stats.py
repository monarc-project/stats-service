#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_restx.inputs import date_from_iso8601

from statsservice.bootstrap import db
from statsservice.models import Stats, Organization
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
parser.add_argument("day", type=int, help="The number of the day of the year.")
parser.add_argument(
    "week", type=int, help="The week of the stats", choices=tuple(range(1, 54))
)
parser.add_argument(
    "month", type=int, help="The month of the stats.", choices=tuple(range(1, 13))
)
parser.add_argument(
    "quarter", type=int, help="The quarter of a year.", choices=(1, 2, 3, 4)
)
parser.add_argument(
    "year", type=int, help="Year of the stats. In full format e.g. 2020."
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
        "day": fields.Integer(description="Number of the day of the year."),
        "week": fields.Integer(description="Week of the stats."),
        "month": fields.Integer(description="Month of the stats. From 1 to 12."),
        "quarter": fields.Integer(
            description="Number of quarter of a year. Possible values [1,2,3,4]"
        ),
        "year": fields.Integer(
            description="Year of the stats. In full format e.g. 2020."
        ),
        "data": fields.Raw(description="The stats as a dynamic JSON object."),
        "created_at": fields.DateTime(
            readonly=True, description="Created time of the stats."
        ),
        "updated_at": fields.DateTime(
            readonly=True, description="Updated time of the stats."
        ),
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
    """Shows a list of all stats, and lets you POST to add new stats"""

    @stats_ns.doc("list_stats")
    @stats_ns.expect(parser)
    @stats_ns.marshal_list_with(stats_list_fields)
    @stats_ns.response(401, "Authorization needed")
    @auth_func
    def get(self):
        """List all stats"""
        # get the organization token
        token = request.headers.get("X-API-KEY", False)
        organization = Organization.query.filter(Organization.token == token).first()

        args = parser.parse_args()
        offset = args.pop("page", 1) - 1
        limit = args.pop("per_page", 10)
        date_from = args.pop("date_from", False)
        date_to = args.pop("date_to", False)
        args = {k: v for k, v in args.items() if v not in [None, ""]}
        args["org_id"] = organization.id

        result = {
            "data": [],
            "metadata": {"count": 0, "offset": offset, "limit": limit,},
        }

        try:
            query = Stats.query
            # Filter on defined object attributes:
            for arg in args:
                if hasattr(Stats, arg):
                    query = query.filter(getattr(Stats, arg) == args[arg])

            # Filter on URL defined attributes (not present in the object attributes)
            if date_from:
                query = query.filter(
                    Stats.year >= date_from.year,
                    Stats.month >= date_from.month,
                    Stats.day >= date_from.day,
                )
            if date_to:
                query = query.filter(
                    Stats.year <= date_to.year,
                    Stats.month <= date_to.month,
                    Stats.day <= date_to.day,
                )

            # Count the result, then paginate
            count = query.count()
            query = query.limit(limit)
            results = query.offset(offset * limit)
        except Exception as e:
            print(e)

        result["data"] = results
        result["metadata"]["count"] = count

        # TODO: define something that will let the client asks for 'aggregated' results
        if args.get("type", "") == "threat":
            #groups = groups_threats(results)
            average_threats(results)

        return result, 200

    @stats_ns.doc("create_stats")
    @stats_ns.expect([stats])
    @stats_ns.marshal_with(stats, code=201)
    @auth_func
    def post(self):
        """Create a new stats"""
        # set the appropriate organization thanks to the token
        token = request.headers.get("X-API-KEY", False)
        organization = Organization.query.filter(Organization.token == token).first()
        # create the new stats
        news_stats = []
        for stats in stats_ns.payload:
            news_stats.append(Stats(**stats, org_id=organization.id))
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
            Stats.objects(uuid__exact=uuid).delete()
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
