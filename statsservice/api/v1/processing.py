#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta
from flask import request, abort
from flask_restx import Namespace, Resource, fields, abort, reqparse

import statsservice.lib.postprocessors
from statsservice.bootstrap import db
from statsservice.lib import AVAILABLE_POSTPROCESSORS
from statsservice.models import Stats
from statsservice.api.v1.common import auth_func
from statsservice.api.v1.identity import admin_permission

logger = logging.getLogger(__name__)

processing_ns = Namespace("processing", description="processing related operations")


# Argument Parsing
parser = reqparse.RequestParser()
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
    """ """
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
        # offset = args.get("offset", 0)
        # type = args.get("type")
        # aggregation_period = args.get("aggregation_period")
        postprocessor = args.get("postprocessor", "")
        now = datetime.today()
        query = Stats.query.filter(
            Stats.type == "threat", Stats.date >= now - timedelta(days=nb_days)
        )
        if local_stats_only:
            query = query.filter(Stats.client.has(local=True))

        print(nb_days)
        print(local_stats_only)
        result = {}
        try:
            result["data"] = getattr(statsservice.lib.postprocessors, postprocessor)(query.all())
        except AttributeError:
            abort(
                500,
                description="There is no such postprocessor: '{}'.".format(postprocessor),
            )

        print(result)

        return result, 200
