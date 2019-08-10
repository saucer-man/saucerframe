#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from lib.core.Request import request
import sys
import time
import json
from lib.core.common import colorprint
from lib.utils.config import ConfigFileParser
from lib.core.data import paths, conf

API_URL = "https://censys.io/api/v1"


def can_auto_login():
    if UID and SECRET:
        try:
            res = request.get(API_URL + "/data", auth=(UID, SECRET), timeout = 10)
            if res.status_code != 200:
                raise SystemExit
            else:
                return True
        except:
            return False
    else:
        return False


def get_ip(query, page):
    '''
    Return ips and total amount when doing query
    '''
    data = {
        "query": query,
        "page": page,
        "fields": ["ip", "protocols"]
    }

    try:
        res = request.post(API_URL + "/search/ipv4", data=json.dumps(data), auth=(UID, SECRET))
        results = res.json()
        
        if res.status_code != 200:
            colorprint.red("error occurred: %s" % results["error"])
            sys.exit(1)

        # add result in some specific form
        for result in results["results"]:
            conf.target.add(result["ip"])

    except Exception as e:
        colorprint.red(e)


def handle_censys(query, limit, offset):
    global UID
    global SECRET
    UID = ConfigFileParser().censys_UID()
    SECRET = ConfigFileParser().censys_SECRET()
    msg = '[+] Trying to login with credentials in config file: {}.' .format(paths.CONFIG_PATH)
    colorprint.green(msg)
    if not can_auto_login():
        err_msg = '[-] Automatic authorization failed.\n[*] Please input your censys API Key (https://censys.io/account/api).'
        colorprint.cyan(err_msg)
        UID = input('[*] UID > ').strip()
        SECRET = input('[*] SECRET > ').strip()
        if not can_auto_login():
            err_msg = "[-] authorization failed"
            colorprint.red(err_msg)
            sys.exit()

    page_start = int(offset/100) + 1
    page_stop = page_start + int(limit/100) + 1

    for page in range(page_start, page_stop):
        get_ip(query, page)

        # the last loop dont need sleep
        if page < page_stop - 1:
            time.sleep(3)











