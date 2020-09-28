#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to process data for the different kind of stats (threat, risk, etc.).
#
# For new postprocessors please use a name which starts with:
# (threat|risk|vulnerability|...)_
#
# postprocessors are automatically listed in statsservice.lib.AVAILABLE_POSTPROCESSORS
# this variable is for example used in statsservice.api.v1.stats.py
#

from collections import defaultdict

import pandas as pd
from statsservice.lib.utils import groups_threats, tree


def threat_average_on_date(threats_stats):
    """Aggregation and average of threats per date for each threat (accross all risk
    analysis).
    """
    grouped_threats = groups_threats(threats_stats)

    labels = tree()

    # group all threats of all analysis per date
    frames = tree()
    for anr_uuid in grouped_threats:
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            for data in stats:
                # print(data)
                # print(data["date"])

                for i in range(1, 5):
                    # for now we remove the labels before processing the frames
                    if "label"+str(i) in data:
                        #data.pop(label)
                        labels[threat_uuid][i] = data["label"+str(i)]

                # prepare the frames
                if data["date"] in frames[threat_uuid]:
                    frames[threat_uuid][data["date"]].append(data)
                else:
                    frames[threat_uuid][data["date"]] = [data]

    # evaluate the average per day for each threats
    result = tree()
    for threat_uuid in frames:
        for date in frames[threat_uuid]:
            df = pd.DataFrame(frames[threat_uuid][date])
            mean = dict(df.mean())
            result[threat_uuid]['values'][date] = mean
        result[threat_uuid]['labels'] = labels[threat_uuid]

    return result


def vulnerability_average_on_date(vulnerabilities_stats):
    """Aggregation and average of vulnerabilities per date for each vulnerability
    (accross all risk analysis).
    """
    # the structure of the stats for the threats and vulnerabilities is the same
    return threat_average_on_date(vulnerabilities_stats)


def threat_process(threats_stats, aggregation_period=None, group_by_anr=None):
    """Return average for the threats for each risk analysis.
    """
    grouped_threats = groups_threats(threats_stats)
    frames = defaultdict(list)
    result = {}
    for anr_uuid in grouped_threats:
        print("Averages for ANR (for threats): {}".format(anr_uuid))
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            frames[threat_uuid].append(stats)
            df = pd.DataFrame(stats)
            result[threat_uuid] = dict(df.mean())
            print("{} : {}".format(threat_uuid, result[threat_uuid]))
            # print(df.to_html())
            print(df.mean().to_markdown())
            print()

    return result


def risk_process(risks_stats, aggregation_period=None, group_by_anr=0):
    if group_by_anr == 0:
        # TODO: group the results for all the anrs and calculate the average.
        aggregated_data = defaultdict(list)

        return aggregated_data
    # TODO: we will see later with the evolution graph requests,
    # if we need to perform aggregation per week, month etc.

    return risks_stats
