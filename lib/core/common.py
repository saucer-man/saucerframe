#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://xiaogeng.top)
See the file 'LICENSE' for copying permission
"""

import sys
import os.path
from lib.core.setting import BANNER
from lib.core.enums import COLOR
from lib.core.data import paths, conf, cmdLineOptions

class Outputscreen:
    '''
    info-->white
    error-->red
    warning-->
    '''
    def banner(self):
        text = "\033[1;%dm %s \033[0m" % (COLOR.blue, BANNER)
        print(text)

    def info(self, text):
        text = "\033[1;%dm %s \033[0m" % (COLOR.white, text)
        print(text)

    def success(self, text):
        text = "\033[1;%dm %s \033[0m" % (COLOR.green, text)
        print(text)
    
    def warning(self,text):
        text = "\033[1;%dm %s \033[0m" % (COLOR.cyan, text)
        print(text)

    def error(self,text):
        text = "\033[1;%dm %s \033[0m" % (COLOR.red, text)
        print(text)
outputscreen=Outputscreen()

def setpaths():
    """
    Sets absolute paths for project directories and files
    """
    root_path = paths.ROOT_PATH # 根目录
    paths.DATA_PATH = os.path.join(root_path, "data") # datapath
    paths.SCRIPT_PATH = os.path.join(root_path, "scripts")
    paths.OUTPUT_PATH = os.path.join(root_path, "output")
    paths.CONFIG_PATH = os.path.join(root_path, "saucerframe.conf")
    if not os.path.exists(paths.SCRIPT_PATH):
        os.mkdir(paths.SCRIPT_PATH)
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)

    # paths.WEAK_PASS = os.path.join(paths.DATA_PATH, "pass100.txt")
    # paths.LARGE_WEAK_PASS = os.path.join(paths.DATA_PATH, "pass1000.txt")
    # paths.UA_LIST_PATH = os.path.join(paths.DATA_PATH, "user-agents.txt")

    if os.path.isfile(paths.CONFIG_PATH):
        pass
    else:
        msg = 'Config files missing, it may cause an issue.\n'
        outputscreen.error(msg)
        sys.exit(0)
    
    #print(root_path,paths.DATA_PATH,paths.SCRIPT_PATH,paths.OUTPUT_PATH,paths.CONFIG_PATH)
    #print(paths.WEAK_PASS,paths.LARGE_WEAK_PASS,paths.UA_LIST_PATH)



# 将'192.168.1.1 -192.168.1.100'分解成ip地址列表
def gen_ip(ip_range):
    '''
    print (gen_ip('192.18.1.1-192.168.1.3'))
    ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    '''
    # from https://segmentfault.com/a/1190000010324211
    def num2ip (num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))
    
    def ip2num(ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0]<< 24 | ips[1]<< 16 | ips[2] << 8 | ips[3]

    start ,end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start,end+1) if num & 0xff]
    
