#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from configparser import ConfigParser
from lib.core.data import paths
from lib.core.common import outputscreen


class ConfigFileParser:
    @staticmethod
    def _get_option(section, option):
        try:
            cf = ConfigParser()
            cf.read(paths.CONFIG_PATH)
            return cf.get(section=section, option=option)
        except:
            outputscreen.warning('Missing essential options, please check your config-file.')
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

    def google_proxy(self):
        return self._get_option('google', 'proxy')

    def google_developer_key(self):
        return self._get_option('google', 'developer_key')

    def google_engine(self):
        return self._get_option('google', 'search_engine')

    # def CloudEyeApikey(self):
    #     return self._get_option('cloudeye', 'api_key')

    # def ColudEyePersonaldomain(self):
    #     return self._get_option('cloudeye', 'personal_domain')







