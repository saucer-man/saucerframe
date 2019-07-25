#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date:2019/04/18

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
检测信息泄露，协程异步请求
"""

import gevent
from gevent.queue import Queue
from lib.core.data import paths
from lib.core.Request import request
from urllib.parse import urlparse
from plugin.random_ua import get_random_ua

def poc(url):
    # url = "http://www.example.org/default.html?ct=32&op=92&item=98"
    # --> http://www.example.org
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc
    result = []
    payloads = Queue() 
    with open(paths.DATA_PATH + '/source_leak_check_payload.txt') as f:
        for payload in f.read().splitlines():
            payloads.put(payload)
    # 这里设置100个协程，payload有144个
    gevent.joinall([gevent.spawn(bak_scan, url, payloads, result) for i in range(100)])
    if result:
        return result
    else:
        return False

def bak_scan(url, payloads, result):
    headers = {
        "User-Agent":get_random_ua()
        }
    while not payloads.empty():
        payload = payloads.get()
        vulnurl = url + "/" + payload
        try:
            flag = 0
            # 如果是备份文件则不需要下载，只需要head方法获取头部信息即可，否则文件较大会浪费大量的时间
            if 'zip' in payload or 'rar' in payload or 'gz' in payload or 'sql' in payload:
                req = request.head(vulnurl, headers=headers, timeout=5, allow_redirects=False, verify=False)
                # 404页面 'Content-Type': 'application/octet-stream',
                # zip 'application/x-zip-compressed' 'application/zip'
                # rar 'application/octet-stream'  'application/x-rar-compressed'
                # 采用Content-Type过滤，还是有一定误报
                if req.status_code == 200:
                    if 'html' not in req.headers['Content-Type'] and 'image' not in req.headers['Content-Type']:
                        flag = 1
            # 当检验git和svn、hg时则需要验证返回内容，get方法
            else:
                req = request.get(vulnurl, headers=headers, timeout=5, verify=False, allow_redirects=False)
                if req.status_code == 200:
                    if 'svn' in payload:
                        if 'dir' in req.text and 'svn' in req.text:
                            flag = 1
                    elif 'git' in payload:
                        if 'repository' in req.text:
                            flag = 1
                    elif 'hg' in payload:
                        if 'hg' in req.text:
                            flag = 1
                    elif '/WEB-INF/web.xml' in payload:
                        if 'web-app' in req.text:
                            flag = 1
            if flag == 1:
                result.append(vulnurl)
        except Exception as e:
            # print(e)
            continue