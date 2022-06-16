#! /usr/bin/env python
#
# Bridge with a MOSP platform. By default: https://objects.monarc.lu
#
import json
import os
from urllib.parse import urljoin

import pymosp

from statsservice.bootstrap import application


MOSP_API_ENDPOINT = urljoin(application.config["MOSP_URL"], "/api/v2/")


def is_object_published(uuid: str, verbose: bool = False) -> bool:
    """Check if an object has been published on MOSP."""
    mosp = pymosp.PyMOSP(MOSP_API_ENDPOINT, os.getenv("MOSP-TOKEN", ""))
    params = {"uuid": uuid}
    result = mosp.objects(params)
    if 0 != int(result["metadata"]["count"]):
        if verbose:
            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )
            )
        return True
    return False
