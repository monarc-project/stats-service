#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to process data for the different kind of stats (threat, risk, etc.).
#
# For new processor please use a name which starts with:
# (threat|risk|vulnerability|...)_
#
# aggregation processors are automatically listed in statsservice.lib.AVAILABLE_PROCESSORS
# this variable is for example used in statsservice.api.v1.stats.py
#

from collections import defaultdict

import pandas as pd
from statsservice.lib.utils import groups_threats, tree, mean_gen, dict_recursive_walk


def threat_average_on_date(threats_stats):
    """Aggregation and average of threats per date for each threat (accross all risk
    analysis).
    """
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


def vulnerability_average_on_date(vulnerabilities_stats):
    """Aggregation and average of vulnerabilities per date for each vulnerability
    (accross all risk analysis).
    """
    # the structure of the stats for the threats and vulnerabilities is the same
    return threat_average_on_date(vulnerabilities_stats)


def risk_averages(risks_stats):
    """Evaluates the averages for the risks. Averages are evaluated per categories
    (current/residual, informational/operational, low/medium/high)."""
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

    # Initialization of the required generators to process the different means.
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

    # Walk through the set of stats and process the means per categories.
    for stat in risks_stats:
        for cureent_or_residual, risk in stat.data["risks"].items():
            # print(cureent_or_residual)
            for level in risk["informational"]:
                # print(level)
                # print(level['value'])
                result[cureent_or_residual]["informational"][
                    level["level"]
                ] = generators[cureent_or_residual]["informational"][
                    level["level"]
                ].send(
                    level["value"]
                )

            for level in risk["operational"]:
                result[cureent_or_residual]["operational"][level["level"]] = generators[
                    cureent_or_residual
                ]["operational"][level["level"]].send(level["value"])

    return result


def risk_averages_on_date(risks_stats):
    """Evaluates the averages for the risks per date. Averages are evaluated per categories
    (current/residual, informational/operational, low/medium/high)."""
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

    for stat in risks_stats:
        #print(stat.date)
        for cureent_or_residual, risk in stat.data["risks"].items():
            for level in risk["informational"]:
                if (
                    str(stat.date)
                    not in generators[cureent_or_residual]["informational"][
                        level["level"]
                    ]
                ):
                    # Initialization of the required generator to process the mean.
                    gen = mean_gen()
                    gen.send(None)
                    generators[cureent_or_residual]["informational"][level["level"]][
                        str(stat.date)
                    ] = gen

                result[cureent_or_residual]["informational"][level["level"]][
                    str(stat.date)
                ] = generators[cureent_or_residual]["informational"][level["level"]][
                    str(stat.date)
                ].send(
                    level["value"]
                )

            for level in risk["operational"]:
                if (
                    str(stat.date)
                    not in generators[cureent_or_residual]["operational"][
                        level["level"]
                    ]
                ):
                    # Initialization of the required generator to process the mean.
                    gen = mean_gen()
                    gen.send(None)
                    generators[cureent_or_residual]["operational"][level["level"]][
                        str(stat.date)
                    ] = gen

                result[cureent_or_residual]["operational"][level["level"]][
                    str(stat.date)
                ] = generators[cureent_or_residual]["operational"][level["level"]][
                    str(stat.date)
                ].send(
                    level["value"]
                )

    # the final values are now stored in a list
    for cureent_or_residual, risk in result.items():
        for level in risk["informational"]:
            result[cureent_or_residual]["informational"][level] = \
                [{"date": a, "value": b} for a, b in result[cureent_or_residual]["informational"][level].items()]
        for level in risk["operational"]:
            result[cureent_or_residual]["operational"][level] = \
                [{"date": a, "value": b} for a, b in result[cureent_or_residual]["operational"][level].items()]

    return result


def threat_process(threats_stats, aggregation_period=None, group_by_anr=None):
    """Return average for the threats for each risk analysis."""
    grouped_threats = groups_threats(threats_stats)
    frames = defaultdict(list)
    result = {}
    for anr_uuid in grouped_threats:
        print("Averages for ANR (for threats): {}".format(anr_uuid))
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            frames[threat_uuid].append(stats)
            df = pd.DataFrame(stats)
            result[threat_uuid] = dict(df.mean())
            # print("{} : {}".format(threat_uuid, result[threat_uuid]))
            # print(df.to_html())
            # print(df.mean().to_markdown())
            print()

    return result
