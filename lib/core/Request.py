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


class Requests():
    
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

    def request(self, *args, **kwargs):
        return requests.request(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)
    
    def head(self, *args, **kwargs):
        return requests.head(*args, **kwargs)

    def put(self, *args, **kwargs):
        return requests.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return requests.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return requests.delete(*args, **kwargs)

request = Requests()