#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

"""
测试用例
"""

import random
import time
from lib.core.Request import request
import traceback

def poc(url):
    return request.get("http://ipconfig.me/ip").text

