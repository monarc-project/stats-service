#! /usr/bin/env python
#
# Utilities to process data for the different kind of stats (threat, risk, etc.).
#
# For new processor please use a name which starts with:
# (threat|risk|vulnerability|...)_
#
# aggregation processors are automatically listed in statsservice.lib.AVAILABLE_PROCESSORS
# this variable is for example used in statsservice.api.v1.stats
#
from typing import Any

from statsservice.lib.utils import dict_recursive_walk
from statsservice.lib.utils import mean_gen
from statsservice.lib.utils import tree

#
# Processors for threats
#


def threat_average_on_date(threats_stats, processor_params=None) -> list:
    result = []

    averages = tree()
    averages_per_days = tree()

    for stats in threats_stats:
        for elem in stats.data:
            if str(elem["uuid"]) not in averages_per_days:
                # initializes structure for a new object UUID
                new_elem = {
                    "object": str(elem["uuid"]),
                    "labels": {
                        "label1": elem.get("label1", ""),
                        "label2": elem.get("label2", ""),
                        "label3": elem.get("label3", ""),
                        "label4": elem.get("label4", ""),
                    },
                    "values": [],
                    "averages": {},
                }
                result.append(new_elem)

            # initializes the generators
            # generators for averages per days per object
            averages_per_days[str(elem["uuid"])][str(stats.date)]["count"] = mean_gen()
            averages_per_days[str(elem["uuid"])][str(stats.date)][
                "maxRisk"
            ] = mean_gen()
            averages_per_days[str(elem["uuid"])][str(stats.date)][
                "averageRate"
            ] = mean_gen()
            # generators for global averages per object
            averages[str(elem["uuid"])]["count"] = mean_gen()
            averages[str(elem["uuid"])]["maxRisk"] = mean_gen()
            averages[str(elem["uuid"])]["averageRate"] = mean_gen()
            # process the averages
            dict_recursive_walk(
                averages_per_days[str(elem["uuid"])][str(stats.date)], "send", None, {}
            )
            dict_recursive_walk(averages[str(elem["uuid"])], "send", None, {})
            averages_per_days[str(elem["uuid"])][str(stats.date)][
                "count"
            ] = averages_per_days[str(elem["uuid"])][str(stats.date)]["count"].send(
                float(elem["count"])
            )
            averages_per_days[str(elem["uuid"])][str(stats.date)][
                "maxRisk"
            ] = averages_per_days[str(elem["uuid"])][str(stats.date)]["maxRisk"].send(
                float(elem["maxRisk"])
            )
            averages_per_days[str(elem["uuid"])][str(stats.date)][
                "averageRate"
            ] = averages_per_days[str(elem["uuid"])][str(stats.date)][
                "averageRate"
            ].send(
                float(elem["averageRate"])
            )
            averages[str(elem["uuid"])]["count"] = averages[str(elem["uuid"])][
                "count"
            ].send(float(elem["count"]))
            averages[str(elem["uuid"])]["maxRisk"] = averages[str(elem["uuid"])][
                "maxRisk"
            ].send(float(elem["maxRisk"]))
            averages[str(elem["uuid"])]["averageRate"] = averages[str(elem["uuid"])][
                "averageRate"
            ].send(float(elem["averageRate"]))

    # format the result for the client
    for elem in result:
        for date in averages_per_days[str(elem["object"])]:
            elem["values"].append(
                {
                    "count": averages_per_days[str(elem["object"])][date]["count"],
                    "maxRisk": averages_per_days[str(elem["object"])][date]["maxRisk"],
                    "averageRate": averages_per_days[str(elem["object"])][date][
                        "averageRate"
                    ],
                    "date": date,
                }
            )
        elem["averages"] = {
            "count": averages[str(elem["object"])]["count"],
            "maxRisk": averages[str(elem["object"])]["maxRisk"],
            "averageRate": averages[str(elem["object"])]["averageRate"],
        }

    return result


#
# Processors for vulnerabilities
#


def vulnerability_average_on_date(vulnerabilities_stats, processor_params=None) -> list:
    """Aggregation and average of vulnerabilities per date for each vulnerability
    (accross all risk analysis).
    """
    # the structure of the stats for the threats and vulnerabilities is the same
    return threat_average_on_date(vulnerabilities_stats)


#
# Processors for risks
#


def risk_averages(risks_stats, processor_params=None):
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


def risk_averages_on_date(risks_stats, processor_params=None):
    """Evaluates the averages for the risks per date. Averages are evaluated per categories
    (current/residual, informational/operational, low/medium/high).
    Supported parameters:
    - risks_type: informational or operational
    - risks_state: current or residual."""
    processor_params = processor_params if processor_params else {}
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
    }  # type: dict[Any, Any]

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
    }  # type: dict[Any, Any]

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
                key=lambda item: item["date"]
            )

        for level in risk["operational"]:
            result[current_or_residual]["operational"][level] = [
                {"date": a, "value": b}
                for a, b in result[current_or_residual]["operational"][level].items()
            ]

            result[current_or_residual]["operational"][level].sort(
                key=lambda item: item["date"]
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
