#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to process data for the different kind of stats (threat, risk, etc.).
#
# For new processor please use a name which starts with:
# (threat|risk|vulnerability|...)_
#
# aggregation processors are automatically listed in statsservice.lib.AVAILABLE_PROCESSORS
# this variable is for example used in statsservice.api.v1.stats
#

import pandas as pd
from statsservice.lib.utils import groups_threats, tree, mean_gen, dict_recursive_walk

#
# Processors for threats
#


def threat_average_on_date(threats_stats, processor_params={}):
    """Aggregation and average of threats per date for each threat (accross all risk
    analysis).
    """
    assert processor_params is not None, "processor_params parameters can not be None."
    grouped_threats = groups_threats(threats_stats)

    labels = tree()
    frames = tree()
    # group all threats of all analysis per date
    for anr_uuid in grouped_threats:
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            for data in stats:
                for i in ["1", "2", "3", "4"]:
                    # store the labels related to the UUID
                    if data.get("label" + str(i), False):
                        labels[threat_uuid]["label" + i] = data["label" + i]
                    # for now we remove from data the labels before processing the frames
                    if "label" + str(i) in data:
                        data.pop("label" + str(i))

                # prepare the frames
                if data["date"] in frames[threat_uuid]:
                    frames[threat_uuid][data["date"]].append(data)
                else:
                    frames[threat_uuid][data["date"]] = [data]

    result = tree()
    preparedResult = []
    # evaluate the averages per day for each threats
    for threat_uuid in frames:
        result[threat_uuid]["object"] = threat_uuid
        result[threat_uuid]["labels"] = labels[threat_uuid]
        result[threat_uuid]["values"] = []
        for date in frames[threat_uuid]:
            df = pd.DataFrame(frames[threat_uuid][date])
            mean = dict(df.mean())
            mean["date"] = date
            result[threat_uuid]["values"].append(mean)
        # averages for each threat
        df = pd.DataFrame(result[threat_uuid]["values"])
        result[threat_uuid]["averages"] = dict(df.mean())
        preparedResult.append(result[threat_uuid])

    return preparedResult


#
# Processors for vulnerabilities
#


def vulnerability_average_on_date(vulnerabilities_stats, processor_params={}):
    """Aggregation and average of vulnerabilities per date for each vulnerability
    (accross all risk analysis).
    """
    assert processor_params is not None, "processor_params parameters can not be None."
    # the structure of the stats for the threats and vulnerabilities is the same
    return threat_average_on_date(vulnerabilities_stats)


#
# Processors for risks
#


def risk_averages(risks_stats, processor_params={}):
    """Evaluates the averages for the risks. Averages are evaluated per categories
    (current/residual, informational/operational, low/medium/high)."""
    assert processor_params is not None, "processor_params parameters can not be None."
    # Initialization of the structure of the result.
    result = {
        "current": {
            "informational": {
                "Low risks": 0,
                "Medium risks": 0,
                "High risks": 0,
            },
            "operational": {
                "Low risks": 0,
                "Medium risks": 0,
                "High risks": 0,
            },
        },
        "residual": {
            "informational": {
                "Low risks": 0,
                "Medium risks": 0,
                "High risks": 0,
            },
            "operational": {
                "Low risks": 0,
                "Medium risks": 0,
                "High risks": 0,
            },
        },
    }

    # Initialization of the required generators to process the different averages.
    generators = {
        "current": {
            "informational": {
                "Low risks": mean_gen(),
                "Medium risks": mean_gen(),
                "High risks": mean_gen(),
            },
            "operational": {
                "Low risks": mean_gen(),
                "Medium risks": mean_gen(),
                "High risks": mean_gen(),
            },
        },
        "residual": {
            "informational": {
                "Low risks": mean_gen(),
                "Medium risks": mean_gen(),
                "High risks": mean_gen(),
            },
            "operational": {
                "Low risks": mean_gen(),
                "Medium risks": mean_gen(),
                "High risks": mean_gen(),
            },
        },
    }
    dict_recursive_walk(generators, "send", None, {})

    # Walk through the set of stats and process the averages per categories.
    for stat in risks_stats:
        for current_or_residual, risk in stat.data["risks"].items():
            # print(current_or_residual)
            for level in risk["informational"]:
                # print(level)
                # print(level['value'])
                result[current_or_residual]["informational"][
                    level["level"]
                ] = generators[current_or_residual]["informational"][
                    level["level"]
                ].send(
                    level["value"]
                )

            for level in risk["operational"]:
                result[current_or_residual]["operational"][level["level"]] = generators[
                    current_or_residual
                ]["operational"][level["level"]].send(level["value"])

    return result


def risk_averages_on_date(risks_stats, processor_params={}):
    """Evaluates the averages for the risks per date. Averages are evaluated per categories
    (current/residual, informational/operational, low/medium/high).
    Supported parameters:
    - risks_type: informational or operational
    - risks_state: current or residual."""
    assert processor_params is not None, "processor_params parameters can not be None."
    result = {
        "current": {
            "informational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
            "operational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
        },
        "residual": {
            "informational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
            "operational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
        },
    }

    generators = {
        "current": {
            "informational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
            "operational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
        },
        "residual": {
            "informational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
            "operational": {
                "Low risks": {},
                "Medium risks": {},
                "High risks": {},
            },
        },
    }

    params = dict(processor_params)

    if not params.get("risks_type", ""):
        params["risks_type"] = "informational,operational"
    if not params.get("risks_state", ""):
        params["risks_state"] = "current,residual"

    for stat in risks_stats:
        # print(stat.date)
        for current_or_residual, risk in stat.data["risks"].items():
            # check if client wants backend to process residual or current risks
            if current_or_residual not in params["risks_state"]:
                continue

            # check if client wants backend to process informational risks
            if "informational" in params["risks_type"]:
                for level in risk["informational"]:
                    if (
                        str(stat.date)
                        not in generators[current_or_residual]["informational"][
                            level["level"]
                        ]
                    ):
                        # Initialization of the required generator to process the average.
                        gen = mean_gen()
                        gen.send(None)
                        generators[current_or_residual]["informational"][
                            level["level"]
                        ][str(stat.date)] = gen

                    # Updates the appropriate average
                    result[current_or_residual]["informational"][level["level"]][
                        str(stat.date)
                    ] = generators[current_or_residual]["informational"][
                        level["level"]
                    ][
                        str(stat.date)
                    ].send(
                        level["value"]
                    )

            # check if client wants backend to process operational risks
            if "operational" in params["risks_type"]:
                for level in risk["operational"]:
                    if (
                        str(stat.date)
                        not in generators[current_or_residual]["operational"][
                            level["level"]
                        ]
                    ):
                        # Initialization of the required generator to process the average.
                        gen = mean_gen()
                        gen.send(None)
                        generators[current_or_residual]["operational"][level["level"]][
                            str(stat.date)
                        ] = gen

                    # Updates the appropriate average
                    result[current_or_residual]["operational"][level["level"]][
                        str(stat.date)
                    ] = generators[current_or_residual]["operational"][level["level"]][
                        str(stat.date)
                    ].send(
                        level["value"]
                    )

    # The final values are now stored in a list
    for current_or_residual, risk in result.items():
        for level in risk["informational"]:
            result[current_or_residual]["informational"][level] = [
                {"date": a, "value": b}
                for a, b in result[current_or_residual]["informational"][level].items()
            ]

            result[current_or_residual]["informational"][level].sort(
                key=lambda
                item:item["date"]
            )

        for level in risk["operational"]:
            result[current_or_residual]["operational"][level] = [
                {"date": a, "value": b}
                for a, b in result[current_or_residual]["operational"][level].items()
            ]

            result[current_or_residual]["operational"][level].sort(
                key=lambda
                item:item["date"]
            )

    # Filter out from the result things that were not processed based on the params
    # these values are empty (set to zero) so useless for the client
    if "current" not in params["risks_state"]:
        result.pop("current")
    elif "informational" not in params["risks_type"]:
        result["current"].pop("informational")
    elif "operational" not in params["risks_type"]:
        result["current"].pop("operational")

    if "residual" not in params["risks_state"]:
        result.pop("residual")
    elif "informational" not in params["risks_type"]:
        result["residual"].pop("informational")
    elif "operational" not in params["risks_type"]:
        result["residual"].pop("operational")

    return result
