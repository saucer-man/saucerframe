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
    time.sleep(0.1)
    if random.randint(1, 10000) > 9998:
        return True
    return False
