#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, abort
from flask_restx import Namespace, Resource, fields, abort

from statsservice.bootstrap import db
from statsservice.lib import AVAILABLE_POSTPROCESSORS
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


# Response marshalling
processedData_list_fields = processing_ns.model(
    "StatsList",
    {
        "processedData": fields.Raw(
            description="Result of the selected postprocessor applied to the resulting stats."
        ),
    },
)


@stats_ns.route("/")
class ProcessingList(Resource):
    """ """

    @processing_ns.doc("list_stats")
    @processing_ns.expect(parser)
    @processing_ns.marshal_list_with(stats_list_fields)
    # @processing_ns.response(401, "Authorization needed")
    # @auth_func
    def get(self):
        """List all stats"""
        args = parser.parse_args(strict=True)
        limit = args.get("limit", 0)
        offset = args.get("offset", 0)
        type = args.get("type")
        # aggregation_period = args.get("aggregation_period")
        postprocessor = args.get("postprocessor", "")
        group_by_anr = args.get("group_by_anr")
        anrs = args.get("anrs")

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

        if limit > 0:
            query = query.limit(limit)
            results = query.offset(offset)
            result["metadata"]["count"] = results.count()
        else:
            results = query.all()
            result["metadata"]["count"] = len(results)

        result["data"] = results  # result without changes from the postprocessor

        # eventually apply a postprocessor with the result
        if postprocessor:
            if not postprocessor.startswith(type + "_"):
                abort(
                    500,
                    Error="Postprocessor '{}' can not be used with type '{}'.".format(
                        postprocessor, type
                    ),
                )
            try:
                processed_result = getattr(
                    statsservice.lib.postprocessors, postprocessor
                )(results)
                # the result of the postprocessor is set in result["processedData"]
                result["processedData"] = processed_result
            except AttributeError:
                abort(
                    500,
                    Error="There is no such postprocessor: '{}'.".format(postprocessor),
                )

        return result, 200
