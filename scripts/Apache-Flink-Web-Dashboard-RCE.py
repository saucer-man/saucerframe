#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

"""
Apache Flink任意Jar包上传导致远程代码执行
"""

from urllib.parse import urlparse
from lib.core.Request import request
import traceback

def poc(url):
    if not url.startswith("http"):
        url = "http://" + url
    o = urlparse(url)
    port = o.port if o.port else 8081
    try:
        target = f"{o.scheme}://{o.hostname}:{port}"
        # print(target)
        res = request.get(url=target, timeout=5)
        if "apache flink" in res.text.lower():
            return True
        else:
            return False
    except:
        return False


