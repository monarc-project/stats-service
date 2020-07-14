#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to process data for the different kind of stats (threats, risks, etc.).
#

from collections import defaultdict

import pandas as pd
from statsservice.lib.utils import groups_threats


def process_threat(threats):
    """Groups stats about threats per ANR (UUID) then per threat UUID."""
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
