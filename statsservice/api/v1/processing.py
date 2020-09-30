#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from flask_restx import Namespace, Resource, fields, abort, reqparse

import statsservice.lib.processors
from statsservice.lib import AVAILABLE_PROCESSORS
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
    "processor",
    type=str,
    help="The processor to apply to a list of stats.",
    required=True,
    choices=tuple(AVAILABLE_PROCESSORS),
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
            description="Result of the selected processor applied to the resulting stats."
        ),
    },
)


@processing_ns.route("/")
class ProcessingList(Resource):
    """Only implements GET method to return the result of a processor."""
    @processing_ns.doc("processing_list")
    @processing_ns.expect(parser)
    @processing_ns.marshal_list_with(processedData_list_fields)
    # @processing_ns.response(401, "Authorization needed")
    # @auth_func
    def get(self):
        """Return the result of the processor."""
        args = parser.parse_args(strict=True)
        nb_days = args.get("nbdays")
        local_stats_only = args.get("local_stats_only", 0)
        type = args.get("type")
        processor = args.get("processor", "")
        now = datetime.today()

        if not processor.startswith(type + "_"):
            abort(
                400,
                Error="Processor '{}' can not be used with type '{}'.".format(
                    processor, type
                ),
            )

        query = Stats.query.filter(
            Stats.type == type, Stats.date >= now - timedelta(days=nb_days)
        )

        if local_stats_only:
            query = query.filter(Stats.client.has(local=True))

        result = {}
        try:
            result["data"] = getattr(statsservice.lib.processors, processor)(query.all())
        except AttributeError:
            abort(
                500,
                description="There is no such processor: '{}'.".format(processor),
            )

        return result, 200
