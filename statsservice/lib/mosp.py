#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Bridge with a MOSP platform. By default: https://objects.monarc.lu
#

import requests

from urllib.parse import urljoin
from statsservice.bootstrap import application


MOSP_API_OBJECT_ENDPOINT = urljoin(application.config["MOSP_URL"], "/object/")


def is_objects_published(uuid):
    """Check if an object has been published on MOSP."""
    r = requests.get(urljoin(MOSP_API_OBJECT_ENDPOINT, uuid))
    if r.status_code == 200:
        return True
    return False
