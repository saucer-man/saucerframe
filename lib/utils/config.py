#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from configparser import ConfigParser
from lib.core.data import paths
from lib.core.common import colorprint


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser()
            cf.read(paths.CONFIG_PATH)
            return cf.get(section=section, option=option)
        except:
            colorprint.cyan('Missing essential options, please check your config-file.')
            return ''

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def fofa_email(self):
        return self._get_option('fofa','email')

    def fofa_key(self):
        return self._get_option('fofa','key')

    def shodan_apikey(self):
        return self._get_option('shodan', 'api_key')

    def censys_UID(self):
        return self._get_option('censys', 'UID')

    def censys_SECRET(self):
        return self._get_option('censys', 'SECRET')
    
    def proxy(self):
        return self._get_option('proxy','proxy')






