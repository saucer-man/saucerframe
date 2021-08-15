import requests
from urllib.parse import urlparse
import socket

def poc(url):
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    host = socket.gethostbyname(o.hostname)
    port = o.port if o.port else 5984
    try:
        url = f"http://{host}:{port}"
        r = requests.get(url, timeout=5, allow_redirects=True, verify=False)
        if "couchdb" in r.text:
            return True
    except:
        pass
    return False