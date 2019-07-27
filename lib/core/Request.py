#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""


import requests
import urllib3
import socks
import socket
from lib.core.data import conf
from plugin.random_ua import get_random_ua

class Requests:
    
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()
    
        if conf.proxy:
            protocol, ip, port = conf.proxy
            if protocol == "socks5":
                socks.set_default_proxy(socks.SOCKS5, ip, port)
            elif protocol == "socks4":
                socks.set_default_proxy(socks.SOCKS4, ip, port)
            else:
                socks.set_default_proxy(socks.HTTP, ip, port)
            socket.socket = socks.socksocket

    def __getattr__(self, method):
        def inner(*args, **kwargs):
            # setting random user agent
            if "headers" not in kwargs.keys():
                kwargs['headers'] = {'User-Agent': get_random_ua()}
            elif 'User-Agent' not in kwargs['headers'].keys():
                kwargs['headers']['User-Agent'] = get_random_ua()

            # setting exclude ssl
            if "verify" not in kwargs.keys():
                kwargs['verify'] = False

            f = getattr(requests, method)
            return f(*args, **kwargs)
        return inner

request = Requests()