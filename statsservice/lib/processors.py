#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to process data for the different kind of stats (threat, risk, etc.).
#

from collections import defaultdict

import pandas as pd
from statsservice.lib.utils import groups_threats


def process_threat(threats_stats, aggregation_period, group_by_anr):
    """Launch the process for stats of type threat."""
    grouped_threats = groups_threats(threats)
    frames = defaultdict(list)

    for anr_uuid in grouped_threats:
        print("Averages for ANR (for threats): {}".format(anr_uuid))
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            frames[threat_uuid].append(stats)
            df = pd.DataFrame(stats)
            result = dict(df.mean())
            if True:  # threat_uuid == 'b402d4e0-4576-11e9-9173-0800277f0571':
                print("{} : {}".format(threat_uuid, result))
        print()


def process_risk(risks_stats, aggregation_period, group_by_anr):
    aggregated_data = defaultdict(list)

    if group_by_anr == 0:
        return aggregated_data

    for risk_stats in risks_stats:
        if aggregated_data[risk_stats.anr] not in aggregated_data.keys():
            if aggregation_period == "day":
                # TODO: get day
                aggregation_value = risk_stats.date
            elif aggregation_period == "week":
                # TODO:
                aggregation_value = risk_stats.date
            elif aggregation_period == "month":
                # TODO:
                aggregation_value = risk_stats.date
            elif aggregation_period == "month":
                # TODO:
                aggregation_value = risk_stats.date
            elif aggregation_period == "quarter":
                # TODO:
                aggregation_value = risk_stats.date
            elif aggregation_period == "year":
                # TODO:
                aggregation_value = risk_stats.date

            aggregated_data[risk_stats.anr] = [
                "anr": risk_stats.anr,
                "type": risk_stats.type,
                "date": aggregation_value,
                "data": []
            ]
        for data in risk_stats.data:
            # TODO: calculate average based on aggregation_period.
            groups[risk_stats.anr]['data'].append(data)

