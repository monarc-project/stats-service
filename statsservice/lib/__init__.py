#! /usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import getmembers, isfunction

from statsservice.lib import postprocessors

# Get all available postprocessors.
AVAILABLE_POSTPROCESSORS = [
    mem[0]
    for mem in getmembers(postprocessors, isfunction)
    if mem[1].__module__ == postprocessors.__name__
]
