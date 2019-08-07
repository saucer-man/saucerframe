#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# description: redis未授权访问

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import socket
from urllib.parse import urlparse
import traceback


def poc(url):
    try:
        socket.setdefaulttimeout(5)

        if not url.startswith("http"):
            url = "http://" + url
        o = urlparse(url)

        host = socket.gethostbyname(o.hostname)
        port = int(o.port) if o.port else 6379

        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
        s = socket.socket()
        s.connect((host, port))
        s.send(payload.encode('utf-8'))
        recv_data = s.recv(1024)
        s.close()
        if recv_data and b'redis_version' in recv_data:
            return "{}:{}".format(host, port)
    except:
        # traceback.print_exc()
        return False
