#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from flask_restx import abort

from statsservice.models import Organization


def auth_func(func):
    def wrapper(*args, **kwargs):
        if "X-API-KEY" in request.headers:
            token = request.headers.get("X-API-KEY", False)
            if token:
                organization = Organization.query.filter(
                    Organization.token == token
                ).first()
                if not organization:
                    abort(401, Error="Authentication required.")
        else:
            abort(401, Error="Authentication required.")
        return func(*args, **kwargs)

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
