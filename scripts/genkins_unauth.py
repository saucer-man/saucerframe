from lib.core.Request import request
from plugin.target_parse  import get_standard_url
# genkins未授权访问

def poc(url):
    try:
        payload = f"{get_standard_url(url)}/manage"
        r = request.get(payload, allow_redirects=False, verify=False)
        if "genkins" in r.text:
            return True
    except:
        # traceback.print_exc()
        pass
    return False