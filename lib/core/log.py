#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
import sys
import logging

logger = logging.getLogger("saucerframe")
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = logging.Formatter("\r[%(asctime)s][%(levelname)s] %(message)s", "%H:%M:%S")
LOGGER_HANDLER.setFormatter(FORMATTER)
logger.addHandler(LOGGER_HANDLER)


