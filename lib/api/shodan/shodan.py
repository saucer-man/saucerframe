#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://xiaogeng.top)
See the file 'LICENSE' for copying permission
"""

import sys
from lib.core.data import paths,conf
from lib.core.common import outputscreen
from lib.utils.config import ConfigFileParser
try:
    import shodan
    from shodan.exception import APIError
except:
    outputscreen.error("Can't import shodan")
    outputscreen.error("Try pip install shodan")
    sys.exit()



class ShodanBase:
    def __init__(self, query, limit, offset):
        self.query = query
        self.limit = limit
        self.offset = offset
        self.api_key = None

    def login(self):
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        outputscreen.info(msg)
        self.api_key = ConfigFileParser().shodan_apikey()

        if not self.api_key:
            msg = 'Automatic authorization failed.'
            outputscreen.warning(msg)
            msg = 'Please input your Shodan API Key (https://account.shodan.io/).'
            outputscreen.info(msg)
            self.api_key = input('API KEY > ').strip()

    def account_info(self):
        try:
            api = shodan.Shodan(self.api_key)
            account_info = api.info()
            msg = "Available Shodan query credits: %d" % account_info.get('query_credits')
            outputscreen.info(msg)
        except APIError as e:
            outputscreen.error(e)
            sys.exit()
        return True

    def api_query(self):
        try:
            api = shodan.Shodan(self.api_key)
            result = api.search(query=self.query, offset=self.offset, limit=self.limit)
        except APIError as e:
            outputscreen.error(e)
            sys.exit()

        if 'matches' in result:
            for match in result.get('matches'):
                conf.target.put(match.get('ip_str') + ':' + str(match.get('port')))
        else:
            pass


def handle_shodan(query, limit, offset):
    s = ShodanBase(query, limit, offset)
    s.login()
    s.account_info()
    s.api_query()
