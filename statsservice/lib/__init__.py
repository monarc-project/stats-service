#! /usr/bin/env python
# -*- coding: utf-8 -*-

from inspect import getmembers, isfunction

from statsservice.lib import processors

# Get all available postrocessors.
AVAILABLE_PROCESSORS = [
    mem[0]
    for mem in getmembers(processors, isfunction)
    if mem[1].__module__ == processors.__name__
]

AVAILABLE_PROCESSORS_FUNC = [
    mem
    for mem in getmembers(processors, isfunction)
    if mem[1].__module__ == processors.__name__
]
