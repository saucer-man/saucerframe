#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
"""
蓝海卓越计费管理系统 debug.php 存在命令调试页面，导致攻击者可以远程命令执行
http://wiki.peiqi.tech/PeiQi_Wiki/Web%E5%BA%94%E7%94%A8%E6%BC%8F%E6%B4%9E/%E6%98%9F%E9%94%90%E8%93%9D%E6%B5%B7/%E8%93%9D%E6%B5%B7%E5%8D%93%E8%B6%8A%E8%AE%A1%E8%B4%B9%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%20debug.php%20%E8%BF%9C%E7%A8%8B%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E.html
"""
from plugin.target_parse import get_standard_url
from lib.core.Request import request


def poc(url):
    url = get_standard_url(url)
    url = url + "/debug.php"
    try:
        r = request.get(url, timeout=5)
        if r.status_code == 200:
            return True
    except:
        pass
    return False
