#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to generate aggregated data.
#

from collections import defaultdict


def tree():
    """Autovivification.
    """
    return defaultdict(tree)


def aggregate_risks():
    pass


def groups_threats(threats):
    """Groups stats about threats per ANR (UUID) then per threat UUID."""
    groups = tree()
    for threat_stats in threats:
        for data in threat_stats.data:
            #groups[threat_stats.anr].append(data)
            if data["uuid"] not in groups[threat_stats.anr].keys():
                groups[threat_stats.anr][data["uuid"]] = []
            groups[threat_stats.anr][data["uuid"]].append(data)
    return groups
