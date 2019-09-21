#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# date:2019/09/13

"""
1. 解析url
2. url->ip
"""
from urllib.parse import urlparse
import socket


def get_standard_url(url):
    """
    url: http://www.baidu.com:80/index.php?id=1&uid=2
    return: http://www.baidu.com:80
    """
    if not url.startswith("http"):
        url = "http://" + url
    o = urlparse(url)  # ParseResult(scheme='http', netloc='www.baidu.com:80', path='/index.php',
                       # params='', query='id=1&uid=2', fragment='')
    return "{}://{}".format(o.scheme, o.netloc)


def url2ip(url):
    """
    url: http://www.baidu.com:80/index.php?id=1&uid=2
    return ['14.215.177.39', '14.215.177.38']
    """
    if not url.startswith("http"):
        url = "http://" + url
    o = urlparse(url)
    domain = o.hostname
    ip = socket.gethostbyname_ex(domain)
    return ip[2]

# print(get_standard_url("http://www.baidu.com:80/index.php?id=1&uid=2")) 
# --> http://www.baidu.com:80
# print(url2ip("http://www.baidu.com:80/index.php?id=1&uid=2"))
# -->['14.215.177.39', '14.215.177.38']


 
