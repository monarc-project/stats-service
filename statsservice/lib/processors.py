#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to generate aggregated data.
#

from collections import defaultdict


def aggregate_risks():
    pass

def aggregate_threats(threats):
    groups = defaultdict(list)
    for threat_stats in threats:
        for data in threat_stats.data:
            print(data)
            groups[data['anr']].append(data)
