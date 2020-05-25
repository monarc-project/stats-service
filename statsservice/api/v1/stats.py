#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from statsservice.api.v1.common import auth_func
from statsservice.documents import Stats, Organization


stats_ns = Namespace("stats", description="stats related operations")


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("organization", type=str, help="Organization of the stats")
parser.add_argument("anr", type=str, help="The ANR UUID  of this stats.")
parser.add_argument(
    "type",
    type=str,
    help="Type of the stats (risk, vulnerability, threat, cartography or compliance)",
)
parser.add_argument("day", type=int, help="Number of the day of the year.")
parser.add_argument("week", type=int, help="Week of the stats")
parser.add_argument("month", type=int, help="Month of the stats. From 1 to 12.")
parser.add_argument(
    "quarter", type=int, help="Number of quarter of a year. Possible values [1,2,3,4]"
)
parser.add_argument(
    "year", type=int, help="Year of the stats. In full format e.g. 2020."
)

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    "page", type=int, required=False, default=1, help="Page number"
)
pagination_parser.add_argument(
    "per_page", type=int, required=False, default=10, help="Page size"
)


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
        "created_at": fields.DateTime(description="Created time of the stats."),
        "updated_at": fields.DateTime(description="Updated time of the stats."),
    },
)

stats_list_fields = stats_ns.model(
    "StatsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects.).",
        ),
        "data": fields.List(fields.Nested(stats), description="List of stats objects"),
    },
)


@stats_ns.route("/")
class StatsList(Resource):
    """Shows a list of all stats, and lets you POST to add new stats"""

    @stats_ns.doc("list_stats")
    @stats_ns.expect(parser)
    @stats_ns.expect(pagination_parser)
    @stats_ns.marshal_list_with(stats_list_fields, skip_none=True)
    @stats_ns.response(401, "Authorization needed")
    @auth_func
    def get(self):
        """List all stats"""
        # get the organization token
        token = request.headers.get("X-API-KEY", False)
        organization = Organization.objects.get(token__exact=token)

        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        args["organization"] = organization

        pagination_args = pagination_parser.parse_args()
        offset = pagination_args.get("offset", 1)
        limit = pagination_args.get("limit", 10)

        result = {
            "data": [],
            "metadata": {"total": 0, "count": 0, "offset": offset, "limit": limit,},
        }

        try:
            total = Stats.objects(**args).count()
            stats = Stats.objects(**args).paginate(page=offset, per_page=limit)
            count = len(stats.items)
        except Organization.DoesNotExist:
            return result, 200
        except Exception as e:
            print(e)
        finally:
            if not total:
                print(result)
                return result, 200

        result["data"] = stats.items
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200

    @stats_ns.doc("create_stats")
    @stats_ns.expect(stats)
    @stats_ns.marshal_with(stats, code=201)
    @auth_func
    def post(self):
        """Create a new stats"""
        # set the appropriate organization thanks to the token
        token = request.headers.get("X-API-KEY", False)
        organization = Organization.objects.get(token__exact=token)
        stats_ns.payload["organization"] = organization
        # create the stats
        new_stat = Stats(**stats_ns.payload)
        return new_stat.save(), 201


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
        return Stats.objects.get(uuid__exact=uuid), 200

    @stats_ns.doc("delete_stats")
    @stats_ns.response(204, "Stats deleted")
    @auth_func
    def delete(self, uuid):
        """Delete a stats given its identifier"""
        # DAO.delete(id)
        return "", 204

    @stats_ns.expect(stats)
    @stats_ns.marshal_with(stats)
    @auth_func
    def put(self, uuid):
        """Update a stats given its identifier"""
        # return DAO.update(id, stats_ns.payload)
        pass
