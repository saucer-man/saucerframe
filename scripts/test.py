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


def poc(str):
    time.sleep(0.1)
    if random.randint(1, 10000) > 9998:
        return True
    return False
