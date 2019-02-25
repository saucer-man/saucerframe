#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import json
import sys

from lib.core.data import paths,conf
from lib.utils.config import ConfigFileParser
from lib.core.common import outputscreen
try:
    import requests
except:
    outputscreen.error("[-] Can't import requests")
    outputscreen.warning("[*] Try pip install requests")
    sys.exit()

class ZoomEye():
    def __init__(self,username=None, password=None):
        self.username = username
        self.password = password
        self.token = ''
        self.zoomeye_dork_api = "https://api.zoomeye.org/{}/search"

    def auto_login(self):
        msg = '[+] Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        outputscreen.success(msg)
        try:
            self.username = ConfigFileParser().ZoomEyeEmail()
            self.password = ConfigFileParser().ZoomEyePassword()
        except:
            pass

        if bool(self.username and self.password):
            if self.get_token():
                return

        msg = '[*] Automatic authorization failed.'
        outputscreen.warning(msg)
        self.manual_login()

    def manual_login(self):
        msg = '[*] Please input your ZoomEye Email and Password below.'
        outputscreen.warning(msg)
        self.username = input('[*] ZoomEye Username(Email): ').strip()
        self.password = input('[*] ZoomEye Password: ').strip()
        if not self.get_token():
            msg = '[-] Error ZoomEye username or password.'
            outputscreen.error(msg)
            sys.exit()

    def get_token(self):
        # Please access https://www.zoomeye.org/api/doc#login
        data = {
        'username' : self.username,
        'password' : self.password
        }
        data_encoded = json.dumps(data)  # dumps 将 python 对象转换成 json 字符串
        res = requests.post('https://api.zoomeye.org/user/login', data=data_encoded)
        if res and res.status_code == 200 and 'access_token' in res.text:
            res_decoded = json.loads(res.text)
            self.token = res_decoded['access_token']
            return self.token
        return False

    def dork_search(self, dork, page=0, resource='web', facet=['ip']):
        """Search records with ZoomEye dorks.

        param: dork
               ex: country:cn
               access https://www.zoomeye.org/search/dorks for more details.
        param: page
               total page(s) number
        param: resource
               set a search resource type, ex: [web, host]
        param: facet
               ex: [app, device]
               A comma-separated list of properties to get summary information
        """
        result = []
        if isinstance(facet, (tuple, list)):
            facet = ','.join(facet)

        zoomeye_api = self.zoomeye_dork_api.format(resource)
        headers = {'Authorization': 'JWT %s' % self.token}
        params = {'query': dork, 'page': page + 1, 'facet': facet}
        resp = requests.get(zoomeye_api, params=params, headers=headers)
        if resp and resp.status_code == 200 and 'matches' in resp.json():
            matches = resp.json().get('matches')
            # total = resp.json().get('total')  # all matches items num
            result = matches

            # Every match item incudes the following information:
            # geoinfo
            # description
            # check_time
            # title
            # ip
            # site
            # system
            # headers
            # keywords
            # server
            # domains

        return result

    def resources_info(self):
        """Resource info shows us available search times.

        host-search: total number of available host records to search
        web-search: total number of available web records to search
        """
        data = None
        zoomeye_api = "https://api.zoomeye.org/resources-info"
        headers = {'Authorization': 'JWT %s' % self.token}
        resp = requests.get(zoomeye_api, headers=headers)
        if resp and resp.status_code == 200 and 'plan' in resp.json():
            data = resp.json()

        return data


def handle_zoomeye(query, limit = 50 , type='host', offset=0):
    z = ZoomEye()
    z.auto_login()
    info = z.resources_info().get('resources')
    if info:
        msg = '[+] Available ZoomEye search: (search:%s)' % (info.get('search', 'NO FOUND'))
        outputscreen.success(msg)
    else:
        msg = '[-] ZoomEye API authorization failed, Please re-run it and enter a new token.'
        outputscreen.error(msg)
        sys.exit()
    # 开始爬取
    limit += offset
    for page_n in range(int(offset / 10), int((limit + 9) / 10)):
        data = z.dork_search(query, page=page_n, resource=type)
        if data:
            for i in data:
                ip_str = i.get('ip')
                if 'portinfo' in i:
                    ip_str = ip_str + ':' + str(i.get('portinfo').get('port'))
                conf.target.put(ip_str)
        else:
            break