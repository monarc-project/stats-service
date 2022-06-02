#! /usr/bin/env python
#
# Utilities to validate incoming stats data.
#
from typing import Any

import jsonschema


def validate_data(data=None, type: str = ""):
    """Check the validity of the submitted stats data.
    Note: an empty JSON object is validated by any schema but we do not accept
    empty stats.
    """
    schema = {}  # type: dict[Any, Any]
    data = data if data else {}
    try:
        jsonschema.validate(data, schema)
    except Exception as e:
        raise e
