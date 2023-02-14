from urllib.parse import urlparse
import requests
import re
def poc(url):
    if not url.startswith("http"):
        url = "http://" + url
    host = urlparse(url).hostname
    port = urlparse(url).port if urlparse(url).port else 80
    port = str(port)
    proxies = {
            "http": f"socks5://{host}:{port}",
            "https": f"socks5://{host}:{port}"
    }

    try:
        res_proxy = requests.get('http://httpbin.org/ip',proxies=proxies,timeout=5).json()
        if res_proxy['origin'] == host:
            return host+":"+ port
    except Exception as e:
        # print(e)
        pass
    return False

if __name__=="__main__":
    print(poc("127.0.0.1:10800"))