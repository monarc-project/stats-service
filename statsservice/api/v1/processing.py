#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from flask_restx import Namespace, Resource, fields, abort, reqparse

import statsservice.lib.postprocessors
from statsservice.lib import AVAILABLE_POSTPROCESSORS
from statsservice.models import Stats

logger = logging.getLogger(__name__)

processing_ns = Namespace("processing", description="Processing related operations on stats data.")


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument(
    "type",
    type=str,
    help="The type of the stats.",
    required=True,
    choices=("risk", "vulnerability", "threat", "cartography", "compliance"),
)
parser.add_argument(
    "postprocessor",
    type=str,
    help="The post-processor to apply to a list of stats.",
    required=True,
    choices=tuple(AVAILABLE_POSTPROCESSORS),
)
parser.add_argument(
    "nbdays", type=int, required=False, default=365, help="Limit of days"
)
parser.add_argument(
    "local_stats_only",
    type=int,
    help="Only on local stats",
    required=False,
    default=1,
    choices=(0, 1),
)


# Response marshalling
processedData_list_fields = processing_ns.model(
    "Result",
    {
        "data": fields.Raw(
            description="Result of the selected postprocessor applied to the resulting stats."
        ),
    },
)


@processing_ns.route("/")
class ProcessingList(Resource):
    """Only implements GET method to return the result of a postprocessor."""
    @processing_ns.doc("processing_list")
    @processing_ns.expect(parser)
    @processing_ns.marshal_list_with(processedData_list_fields)
    # @processing_ns.response(401, "Authorization needed")
    # @auth_func
    def get(self):
        """Return the result of the postprocessor."""
        args = parser.parse_args(strict=True)
        nb_days = args.get("nbdays")
        local_stats_only = args.get("local_stats_only", 0)
        type = args.get("type")
        postprocessor = args.get("postprocessor", "")
        now = datetime.today()

        if not postprocessor.startswith(type + "_"):
            abort(
                400,
                Error="Postprocessor '{}' can not be used with type '{}'.".format(
                    postprocessor, type
                ),
            )

        query = Stats.query.filter(
            Stats.type == type, Stats.date >= now - timedelta(days=nb_days)
        )

        if local_stats_only:
            query = query.filter(Stats.client.has(local=True))

        result = {}
        try:
            result["data"] = getattr(statsservice.lib.postprocessors, postprocessor)(query.all())
        except AttributeError:
            abort(
                500,
                description="There is no such postprocessor: '{}'.".format(postprocessor),
            )

        return result, 200
