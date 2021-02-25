#-*- coding:utf-8 -*-

import random
import requests
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()


TARGET_URI = "/ui/vropspluginui/rest/services/uploadova"

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua

def poc(url):
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc
    headers = {
        'User-Agent': get_ua(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    targetUrl = url + TARGET_URI
    try:
        res = requests.get(targetUrl,
                            headers=headers,
                            timeout=15,
                            verify=False)

        if res.status_code == 405:
            return True      
    except Exception as e:
        pass

    return False