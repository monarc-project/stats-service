#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to generate aggregated statistics (averages, etc.).
#

import pandas as pd
from collections import defaultdict
from statsservice.lib.processors import groups_threats


def tree():
    """Autovivification.
    """
    return defaultdict(tree)


def average_threats(threats):
    """filter, group, and then process the result depends on the stats type.
    """
    grouped_threats = groups_threats(threats)
    frames = defaultdict(list)

    for anr_uuid in grouped_threats:
        print("Averages for ANR (for threats): {}".format(anr_uuid))
        for threat_uuid, stats in grouped_threats[anr_uuid].items():
            frames[threat_uuid].append(stats)
            df = pd.DataFrame(stats)
            result = dict(df.mean())
            if True:#threat_uuid == 'b402d4e0-4576-11e9-9173-0800277f0571':
                print("{} : {}".format(threat_uuid, result))
        print()
