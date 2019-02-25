#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

class COLOR:
    black = 30  #  黑色
    red = 31  #  红色
    green = 32  #  绿色
    yellow = 33  #  黄色
    blue = 34  #  蓝色
    purple = 35  #  紫红色
    cyan = 36  #  青蓝色
    white = 37  #  白色
    
class POC_RESULT_STATUS:
    FAIL = 0
    SUCCESS = 1
    RETRAY = 2

class PROXY_TYPE:  # keep same with SocksiPy(import socks)
    PROXY_TYPE_SOCKS4 = SOCKS4 = 1
    PROXY_TYPE_SOCKS5 = SOCKS5 = 2
    PROXY_TYPE_HTTP = HTTP = 3
    PROXY_TYPE_HTTP_NO_TUNNEL = 4