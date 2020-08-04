#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities.
#

from collections import defaultdict


def tree():
    """Autovivification.
    """
    return defaultdict(tree)


def groups_threats(threats):
    """Groups stats about threats per ANR (UUID) then per threat UUID.
    """
    groups = tree()
    for threat_stats in threats:
        anr_uuid = str(threat_stats.anr)
        for data in threat_stats.data:
            # groups[threat_stats.anr].append(data)
            str_uuid = str(data["uuid"])
            if str_uuid not in groups[anr_uuid].keys():
                groups[anr_uuid][str_uuid] = []
            # add the related date of this stats
            data["date"] = threat_stats.date.strftime("%Y-%m-%d")

            # MONARC send averageRate as a string, so we convert to float
            data["averageRate"] = float(data.get("averageRate", 0))

            for label in ["label1", "label2", "label3", "label4"]:
                if label in data:
                    data.pop(label)

            groups[anr_uuid][str_uuid].append(data)

    return groups


def groups_vulnerabilities(vulnerabilities):
    """Groups stats about vulnerabilities per ANR (UUID) then per vulnerability UUID.
    """
    # the structure of the stats for the threats and vulnerabilities is the same
    return groups_threats(vulnerabilities)
