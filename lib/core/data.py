#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from lib.core.datatype import AttribDict

# saucerframe paths
paths = AttribDict()

# object to store original command line options
cmdLineOptions = AttribDict()

# object to share within function and classes command
# line options and settings
conf = AttribDict()

# object to control engine 
th = AttribDict()