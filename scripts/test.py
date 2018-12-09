#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
测试用例
"""

import random
import time


def poc(str):
    if random.randint(1, 1000) > 998:
        time.sleep(0.3)
        return True
    return False
