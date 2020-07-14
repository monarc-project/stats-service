#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bridge with a MOSP platform. By default: https://objects.monarc.lu
#

import json
import requests

from urllib.parse import urljoin
from statsservice.bootstrap import application


MOSP_API_OBJECT_ENDPOINT = urljoin(application.config["MOSP_URL"], "/api/v2/object/")


def is_object_published(uuid, verbose=False):
    """Check if an object has been published on MOSP."""
    params = {"uuid": uuid}
    r = requests.get(MOSP_API_OBJECT_ENDPOINT, params=params)
    if r.status_code == 200:
        if 0 != int(r.json()["metadata"]["count"]):
            if verbose:
                print(
                    json.dumps(
                        r.json(),
                        ensure_ascii=False,
                        sort_keys=True,
                        indent=4,
                        separators=(",", ": "),
                    )
                )
            return True
    return False
