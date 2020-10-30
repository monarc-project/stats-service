#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sqlalchemy.exc
from flask import request
from flask_login import current_user
from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask_restx.inputs import date_from_iso8601, boolean
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql.expression import desc

from statsservice.bootstrap import db
from statsservice.models import Stats, Client
from statsservice.api.v1.common import auth_func, uuid_type


logger = logging.getLogger(__name__)

stats_ns = Namespace("stats", description="stats related operations")


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument(
    "anr", type=uuid_type, location="json", help="The ANR UUID related to this stats."
)
parser.add_argument(
    "type",
    type=str,
    help="The type of the stats.",
    required=True,
    location="json",
    choices=("risk", "vulnerability", "threat", "cartography", "compliance"),
)
parser.add_argument(
    "group_by_anr",
    type=int,
    help="If the result should be grouped by anr or not.",
    required=False,
    default=1,
    location="json",
    choices=(0, 1),
)
parser.add_argument(
    "date_from",
    type=date_from_iso8601,
    required=False,
    location="json",
    help="The date of the stats must be bigger or equal than this value.",
)
parser.add_argument(
    "date_to",
    type=date_from_iso8601,
    required=False,
    location="json",
    help="The date of the stats must be smaller or equal than this value.",
)
parser.add_argument(
    "anrs",
    required=False,
    location="json",
    type=list,
    help="List of the anrs' uuids to filter by.",
)
parser.add_argument(
    "get_last",
    type=boolean,
    required=False,
    location="json",
    help="Specify that result should compose only the last records in the results set for each anr. Dates filters are ignored in this case.",
)
parser.add_argument(
    "offset",
    type=int,
    required=False,
    location="json",
    default=0,
    help="Start position",
)
parser.add_argument(
    "limit",
    type=int,
    required=False,
    location="json",
    default=0,
    help="Limit of records",
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
        "date": fields.Date(description="The stats date in format 'Y-m-d'"),
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
        args = parser.parse_args(strict=True)
        limit = args.get("limit", 0)
        offset = args.get("offset", 0)
        type = args.get("type")
        group_by_anr = args.get("group_by_anr")
        anrs = args.get("anrs")
        get_last = args.get("get_last")
        date_from = args.get("date_from")
        date_to = args.get("date_to")

        if not get_last:
            if date_from is None:
                date_from = (date.today() + relativedelta(months=-3)).strftime(
                    "%Y-%m-%d"
                )
            if date_to is None:
                date_to = date.today().strftime("%Y-%m-%d")

        result = {
            "data": [],
            "metadata": {"count": 0, "offset": offset, "limit": limit},
        }

        query = Stats.query

        if not current_user.is_admin():
            query = query.filter(Stats.client_id == current_user.id)

        query = query.filter(Stats.type == type)

        if anrs:
            query = query.filter(Stats.anr.in_(anrs))

        if get_last:
            # TODO: Handle the case if the request is from an admin user (from BO).
            # Get all the records grouped by anr with max date.
            results = []
            max_date_and_anrs = (
                query.with_entities(Stats.anr, db.func.max(Stats.date))
                .group_by(Stats.anr)
                .all()
            )
            for max_date_and_anr in max_date_and_anrs:
                results.append(
                    query.filter(
                        Stats.anr == max_date_and_anr[0],
                        Stats.date == max_date_and_anr[1],
                    )
                    .first()
                    ._asdict()
                )
            result["data"] = results
            result["metadata"] = {"count": len(results), "offset": 0, "limit": 0}

            return result, 200

        query = query.filter(Stats.date >= date_from, Stats.date <= date_to)

        if limit or offset:
            results = query.limit(limit).offset(offset)
            result["metadata"]["count"] = results.count()
        else:
            results = query.all()
            result["metadata"]["count"] = len(results)

        result["data"] = results

        return result, 200

    @stats_ns.doc("create_stats")
    @stats_ns.expect([stats])
    @stats_ns.marshal_list_with(stats_list_fields, code=201)
    @stats_ns.response(401, "Authorization needed")
    @auth_func
    def post(self):
        """Create a new stats"""
        result = {
            "data": [],
            "metadata": {"count": 0, "offset": 0, "limit": 0},
        }
        errors = []
        for stats in stats_ns.payload:
            try:
                new_stat = Stats(**stats, client_id=current_user.id)
                db.session.add(new_stat)
                db.session.commit()
                result["data"].append(new_stat)
                result["metadata"]["count"] += 1
            except (
                sqlalchemy.exc.IntegrityError,
                sqlalchemy.exc.InvalidRequestError,
            ) as e:
                logger.error("Duplicate stats {}".format(stats["uuid"]))
                errors.append(stats["uuid"])
                db.session.rollback()

        # if some objects can not created we return the HTTP code 207 (Multi-Status)
        # if all objects of the batch POST request are created we simply return 201.
        return result, 207 if errors else 201


@stats_ns.route("/<string:anr>")
@stats_ns.response(404, "Stats not found")
class StatsItem(Resource):
    """Show the stats items by anr resource and lets you delete it"""

    @stats_ns.doc("get_stats")
    @stats_ns.marshal_with(stats)
    @auth_func
    def get(self, anr):
        """Fetch a given resource by anr"""

        return Stats.query.filter(Stats.anr == anr).all(), 200

    @stats_ns.doc("delete_stats")
    @stats_ns.response(204, "Stats deleted")
    @auth_func
    def delete(self, anr):
        """Delete stats by provided anr"""
        try:
            Stats.query.filter(Stats.anr == anr).delete()
            db.session.commit()
            return "", 204
        except:
            db.session.rollback()
            abort(500, Error="Impossible to delete the stats.")
