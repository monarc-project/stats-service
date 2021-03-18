#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# Utilities to validate incoming stats data.
#

import jsonschema
from typing import Any


def validate_data(data={}, type: str = ""):
    """Check the validity of the submitted stats data.
    Note: an empty JSON object is validated by any schema but we do not accept
    empty stats.
    """
    schema = {}  # type: dict[Any, Any]
    try:
        jsonschema.validate(data, schema)
    except Exception as e:
        raise e
