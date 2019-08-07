#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date:2019/06/16

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
# mongodb no certification required

import socket
from urllib.parse import urlparse
import binascii
import traceback


def poc(url):
    # url = "http://www.example.org:22222/default.html?ct=32&op=92&item=98"
    # --> host:www.example.org   port:22222
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    host = socket.gethostbyname(o.hostname)
    port = o.port if o.port else 27017
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))  # if port are not open there will raise
        data = binascii.a2b_hex("430000000300000000000000d40700000000000061646d696e2e24636d640000000000"
                                "ffffffff1c000000016c69737444617461626173657300000000000000f03f00")
        s.send(data)
        result = s.recv(500)  # if not mongo there will raise
        if "databases".encode('utf-8') in result:
            return "{}:{}".format(host, port)
        return False
        
    except:
        # traceback.print_exc()
        return False
