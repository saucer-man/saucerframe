from lib.core.data import paths
import requests

def poc(url):
    if 'http' not in url:
        url = 'http://' + url

    with open(paths.DATA_PATH + '/source_leak_check_payload.txt') as f:
        payloads = f.read().splitlines()

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
    for payload in payloads:
        vulnurl = url + payload
        # print("test %s"% vulnurl)
        try:
            flag = 0
            # 如果是备份文件则不需要下载，只需要head方法获取头部信息即可，否则文件较大会浪费大量的时间
            if 'zip' in payload or 'rar' in payload or 'gz' in payload or 'sql' in payload:
                req = requests.head(vulnurl, headers=headers, timeout=3, allow_redirects=False, verify=False)

                if req.status_code == 200:
                    if 'html' not in req.headers['Content-Type'] and 'image' not in req.headers['Content-Type']:
                        flag = 1
            # 当检验git和svn、hg时则需要验证返回内容，get方法
            else:
                req = requests.get(vulnurl, headers=headers, timeout=3, verify=False, allow_redirects=False)
                if req.status_code == 200:
                    if 'svn' in payload:
                        if 'dir' in req.content and 'svn' in req.content:
                            flag = 1
                    elif 'git' in payload:
                        if 'repository' in req.content:
                            flag = 1
                    elif 'hg' in payload:
                        if 'hg' in req.content:
                            flag = 1
                    elif '/WEB-INF/web.xml' in payload:
                        if 'web-app' in req.content:
                            flag = 1

            if flag == 1:
                return vulnurl

        except Exception as e:
            return 0
    return 0