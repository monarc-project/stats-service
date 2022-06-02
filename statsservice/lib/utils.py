#! /usr/bin/env python
#
# Utilities.
#
import hashlib
import json
from collections import defaultdict
from typing import Any
from typing import Dict


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
    for _key, value in dictionary.items():
        if type(value) is dict:
            dict_recursive_walk(value, func, *args, **kwargs)
        else:
            if hasattr(value, func):
                getattr(value, func)(args[0])


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def tree():
    """Autovivification."""
    return defaultdict(tree)


def groups_threats(threats):
    """Groups stats about threats per ANR (UUID) then per threat UUID.
    Function not used."""
    groups = tree()
    for threat_stats in threats:
        anr_uuid = str(threat_stats.anr)
        for data in threat_stats.data:
            # groups[threat_stats.anr].append(data)
            try:  # temporary try
                str_uuid = str(data["uuid"])
            except Exception:
                continue
            if str_uuid not in groups[anr_uuid].keys():
                groups[anr_uuid][str_uuid] = []
            # add the related date of this stats
            data["date"] = threat_stats.date.strftime("%Y-%m-%d")

            # MONARC send averageRate as a string, so we convert to float
            data["averageRate"] = float(data.get("averageRate", 0))

            groups[anr_uuid][str_uuid].append(data)

    return groups


def groups_vulnerabilities(vulnerabilities):
    """Groups stats about vulnerabilities per ANR (UUID) then per vulnerability UUID.
    Function not used."""
    # the structure of the stats for the threats and vulnerabilities is the same
    return groups_threats(vulnerabilities)


# def groups_risks(risks):
#     groups = tree()
