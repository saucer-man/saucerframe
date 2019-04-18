# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import sys
from lib.core.data import paths,conf
from lib.core.common import outputscreen
from lib.utils.config import ConfigFileParser
from shodan import Shodan, APIError

class ShodanBase:
    def __init__(self, query, limit, offset):
        self.query = query
        self.limit = limit
        self.offset = offset
        self.api_key = None

    def login(self):
        msg = '[+] Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        outputscreen.success(msg)
        self.api_key = ConfigFileParser().shodan_apikey()

        if not self.api_key:
            msg = '[*] Automatic authorization failed.'
            outputscreen.warning(msg)
            msg = '[*] Please input your Shodan API Key (https://account.shodan.io/).'
            outputscreen.warning(msg)
            self.api_key = input('[*] API KEY > ').strip()

    def account_info(self):
        try:
            if not self.api_key:
                outputscreen.error("[-] Shodan api cant not be Null")
                sys.exit()
            api = Shodan(self.api_key)
            account_info = api.info()
            msg = "[+] Available Shodan query credits: %d" % account_info.get('query_credits')
            outputscreen.success(msg)
        except APIError as e:
            outputscreen.error(e)
            sys.exit()
        return True

    def api_query(self):
        try:
            api = Shodan(self.api_key)
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
