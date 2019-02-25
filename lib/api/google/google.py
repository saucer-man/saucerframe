#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import sys
from lib.core.common import outputscreen
from lib.core.enums import PROXY_TYPE
from lib.utils.config import ConfigFileParser
from lib.core.data import conf
from httplib2 import Http, ProxyInfo
from socket import error as SocketError
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError as ServerHttpDenied
except:
    outputscreen.error("[-] Can't import googleapiclient")
    outputscreen.warning("[*] Try pip install google-api-python-client")
    sys.exit()

def _initHttpClient():
    if conf.google_proxy:
        proxy_str = conf.google_proxy
    elif ConfigFileParser().google_proxy():
        proxy_str = ConfigFileParser().google_proxy()
    else:
        proxy_str = None

    if not proxy_str:
        return Http()

    msg = 'Proxy: %s' % proxy_str
    outputscreen.info(msg)
    proxy = proxy_str.strip().split(' ')
    if len(proxy) != 3:
        msg = '[-] SyntaxError in GoogleProxy string, Please check your args or config file.'
        outputscreen.error(msg)
        sys.exit()
    if proxy[0].lower() == 'http':
        type = PROXY_TYPE.HTTP
    elif proxy[0].lower() == 'sock5':
        type = PROXY_TYPE.SOCKS5
    elif proxy[0].lower() == 'sock4':
        type = PROXY_TYPE.SOCKS4
    else:
        msg = '[-] Invalid proxy-type in GoogleProxy string, Please check your args or config file.'
        outputscreen.error(msg)
        sys.exit()
    try:
        port = int(proxy[2])
    except ValueError:
        msg = '[-] Invalid port in GoogleProxy string, Please check your args or config file.'
        outputscreen.error(msg)
        sys.exit()
    else:
        http_client = Http(proxy_info=ProxyInfo(type, proxy[1], port))
    return http_client


def handle_google(query, limit, offset=0):
    key = ConfigFileParser().google_developer_key()
    engine = ConfigFileParser().google_engine()
    if not key or not engine:
        msg = "[-] Please config your 'developer_key' and 'search_enging' at saucerfram.conf"
        outputscreen.error(msg)
        sys.exit()
    try:
        service = build("customsearch", "v1", http=_initHttpClient(), developerKey=key)

        result_info = service.cse().list(q=query, cx=engine).execute()
        msg = '[+] Max query results: %s' % str(result_info.get('searchInformation',{}).get('totalResults'))
        outputscreen.success(msg)

        ans = set()
        limit += offset
        for i in range(int(offset / 10), int((limit + 10 - 1) / 10)):
            result = service.cse().list(q=query, cx=engine, num=10, start=i * 10 + 1).execute()
            if 'items' in result:
                for url in result.get('items'):
                    ans.add(url.get('link'))
        for t in ans:
            conf.target.put(t)

    except SocketError:
        outputscreen.error('[-] Unable to connect Google, maybe agent/proxy error.')
        sys.exit()
    except ServerHttpDenied as e:
        outputscreen.warning('[-] It seems like Google-Server denied this request.')
        outputscreen.error(e)
        sys.exit()
