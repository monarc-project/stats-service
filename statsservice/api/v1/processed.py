#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from flask_restx import Namespace, Resource, fields, abort, reqparse
from flask_restx.inputs import date_from_iso8601

import statsservice.lib.processors
from statsservice.lib import AVAILABLE_PROCESSORS, AVAILABLE_PROCESSORS_FUNC
from statsservice.api.v1.common import auth_func
from statsservice.models import Stats

logger = logging.getLogger(__name__)

processed_ns = Namespace(
    "processed", description="Processing related operations on stats data."
)


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument(
    "type",
    type=str,
    help="The type of the stats.",
    required=True,
    location="json",
    choices=("risk", "vulnerability", "threat", "cartography", "compliance"),
)
parser.add_argument(
    "processor",
    type=str,
    help="The processor to apply to a list of stats.",
    required=True,
    location="json",
    choices=tuple(AVAILABLE_PROCESSORS),
)
parser.add_argument(
    "processor_params",
    type=dict,
    required=False,
    location="json",
    default={},
    help="Arguments passed to the processor.",
)
parser.add_argument(
    "anrs",
    required=False,
    location="json",
    type=list,
    help="List of the anrs' uuids to filter by.",
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
    "local_stats_only",
    type=int,
    help="Only on local stats",
    required=False,
    location="json",
    default=0,
    choices=(0, 1),
)


# Response marshalling
processedData_list_fields = processed_ns.model(
    "Result",
    {
        "type": fields.String(
            description="Type of the processed stats data (risk, vulnerability, threat, cartography or compliance)."
        ),
        "processor": fields.String(
            description="Processor used for the stats data processing."
        ),
        "data": fields.Raw(
            description="Result of the selected processor applied to the resulting stats."
        ),
    },
)


@processed_ns.route("/")
class ProcessingList(Resource):
    """Only implements GET method to return the result of a processor."""

    @processed_ns.doc("processing_list")
    @processed_ns.expect(parser)
    @processed_ns.marshal_list_with(processedData_list_fields)
    @processed_ns.response(401, "Authorization needed")
    @auth_func
    def get(self):
        """Return the result of the processor."""
        processorParams = {}
        args = parser.parse_args(strict=True)
        date_from = args.get("date_from")
        date_to = args.get("date_to")
        local_stats_only = args.get("local_stats_only", 0)
        stat_type = args.get("type")
        processor = args.get("processor", "")
        processorParams = args.get("processor_params", {})
        anrs = args.get("anrs")
        now = datetime.today()

        if None is processorParams:
            processorParams = {}

        # Test:
        logger.info("START TEST")
        logger.info(processorParams)
        logger.info(date_from)
        logger.info("END TEST")

        if not processor.startswith(stat_type + "_"):
            abort(
                400,
                Error="Processor '{}' can not be used with type '{}'.".format(
                    processor, stat_type
                ),
            )

        query = Stats.query.filter(Stats.type == stat_type)

        if date_from is not None:
            query = query.filter(Stats.date >= date_from)

        if date_to is not None:
            query = query.filter(Stats.date <= date_to)

        if anrs:
            query = query.filter(Stats.anr.in_(anrs))

        if local_stats_only:
            query = query.filter(Stats.client.has(local=True))

        query = query.all()

        result = {
            "type": stat_type,
            "processor": processor,
            "data": [],
        }
        if query:
            try:
                result["data"] = getattr(statsservice.lib.processors, processor)(
                    query, processorParams
                )
            except AttributeError:
                abort(
                    500,
                    description="There is no such processor: '{}'.".format(processor),
                )

        return result, 200


@processed_ns.route("/list")
class ProcessorList(Resource):
    """Return the list of available processors with their description."""

    def get(self):
        """Return the list of available processors with their description."""
        return [
            {"name": processor[0], "description": processor[1].__doc__}
            for processor in AVAILABLE_PROCESSORS_FUNC
        ], 200
