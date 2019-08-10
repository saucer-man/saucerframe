#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import sys
import json
import base64
from lib.utils.config import ConfigFileParser
from lib.core.common import colorprint
from lib.core.data import paths, conf
from lib.core.Request import request
from lib.core.log import logger


def check(email, key):  # verify email and key
    if email and key:
        auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            response = request.get(auth_url)
            if response.status_code == 200:
                return True
        except Exception as e:
            logger.debug(e)
            return False
    return False


def handle_fofa(query, limit, offset=0):
    try:
        msg = '[+] Trying to login with credentials in config file: {}.'.format(paths.CONFIG_PATH)
        colorprint.green(msg)
        email = ConfigFileParser().fofa_email()
        key = ConfigFileParser().fofa_key()
        if check(email, key):
            pass
        else:
            raise Exception("Automatic authorization failed")   # will go to except block
    except Exception as e:
        logger.debug(e)
        msg = '[*] Automatic authorization failed.'
        colorprint.cyan(msg)
        msg = '[*] Please input your FoFa Email and API Key below.'
        colorprint.cyan(msg)
        email = input("[*] Fofa Email: ").strip()
        key = input('[*] Fofa API Key: ').strip()
        if not check(email, key):
            msg = '[-] Fofa API authorization failed, Please re-run it and enter a valid key.'
            colorprint.red(msg)
            sys.exit()

    query = base64.b64encode(query.encode('utf-8')).decode('utf-8')
    
    # count how many result to search
    size = limit + offset  
    
    url = f"https://fofa.so/api/v1/search/all?email={email}&key={key}&qbase64={query}&size={size}"
    try:
        response = request.get(url).text
        resp = json.loads(response)
        if not resp["error"]:
            for item in resp.get('results')[offset:]:
                conf.target.add(item[0])

    except Exception as e:
        colorprint.red(e)
        sys.exit()
