#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import os.path
from lib.core.setting import BANNER
from lib.core.data import paths
from thirdlib.colorama import init, Fore, Style

init(autoreset=True)


class ColorPrint:

    @staticmethod
    def white(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.WHITE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def green(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.GREEN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def cyan(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.CYAN + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def red(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.RED + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def blue(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.BLUE + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)

    @staticmethod
    def yellow(s, end='\n', flush=False):
        print(Style.BRIGHT+Fore.YELLOW + str(s) + Fore.RESET+Style.RESET_ALL, end=end, flush=flush)


colorprint = ColorPrint()


def set_paths(root_path):
    """
    Sets absolute paths for project directories and files
    """
    paths.ROOT_PATH = root_path # root path
    paths.DATA_PATH = os.path.join(paths.ROOT_PATH, "data")
    paths.SCRIPT_PATH = os.path.join(paths.ROOT_PATH, "scripts")
    paths.PLUGIN_PATH = os.path.join(paths.ROOT_PATH, "plugin")
    paths.OUTPUT_PATH = os.path.join(paths.ROOT_PATH, "output")
    paths.CONFIG_PATH = os.path.join(paths.ROOT_PATH, "config.conf")
    if not os.path.exists(paths.SCRIPT_PATH):
        err_msg = "script file missing,it may cause some issues."
        colorprint.red(err_msg)
        os.mkdir(paths.SCRIPT_PATH)
    if not os.path.exists(paths.PLUGIN_PATH):
        err_msg = "plugin file missing,it may cause some issues."
        colorprint.red(err_msg)
        os.mkdir(paths.PLUGIN_PATH)
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)

    if os.path.isfile(paths.CONFIG_PATH):
        pass
    else:
        err_msg = 'Config files missing, it may cause some issues.\n'
        colorprint.red(err_msg)


def banner():
    colorprint.blue(BANNER)


def gen_ip(ip_range):
    '''
    print (gen_ip('192.18.1.1-192.168.1.3'))
    ==> ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    from https://segmentfault.com/a/1190000010324211
    '''
    def num2ip(num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))
    
    def ip2num(ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

    start, end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start, end+1) if num & 0xff]
