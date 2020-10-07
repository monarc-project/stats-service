#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities.
#

from collections import defaultdict


def mean_gen():
    """Yields the accumulated mean of sent values.

    >>> g = meangen()
    >>> g.send(None) # Initialize the generator
    >>> g.send(4)
    4.0
    >>> g.send(10)
    7.0
    >>> g.send(-2)
    4.0
    """
    sum = yield (None)
    count = 1
    while True:
        sum += yield (sum / float(count))
        count += 1


def dict_recursive_walk(dictionary, func, *args, **kwargs):
    """Walk recursively in a nested dictionary and apply a function (send()) with
    parameters."""
    for key, value in dictionary.items():
        if type(value) is dict:
            dict_recursive_walk(value, func, *args, **kwargs)
        else:
            if hasattr(value, func):
                getattr(value, func)(args[0])


def tree():
    """Autovivification."""
    return defaultdict(tree)


def groups_threats(threats):
    """Groups stats about threats per ANR (UUID) then per threat UUID."""
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

            groups[anr_uuid][str_uuid].append(data)

    return groups


def groups_vulnerabilities(vulnerabilities):
    """Groups stats about vulnerabilities per ANR (UUID) then per vulnerability UUID."""
    # the structure of the stats for the threats and vulnerabilities is the same
    return groups_threats(vulnerabilities)


def groups_risks(risks):
    groups = tree()
