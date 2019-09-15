#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""


import os
import sys
import time
import re
import logging
import ipaddress
from lib.core.data import paths, conf
from lib.core.common import colorprint, gen_ip
from lib.utils.config import ConfigFileParser
from lib.core.log import logger


def init_options(args):
    check_show(args)
    logger_lever_set(args)
    proxy_regester(args)
    engine_register(args)
    script_register(args)
    target_register(args)
    output_register(args)


def check_show(args):
    # if show scripts 
    if args.show_scripts:
        module_name_list = os.listdir(paths.SCRIPT_PATH)
        colorprint.green('[+] Script Name ')
        order = 1
        for module in module_name_list:
            # only show useful scripts
            if module not in ['__init__.py', 'test.py'] and os.path.splitext(module)[1] == '.py':
                colorprint.green(str(order) + '. ' + module)
                order += 1
        msg = '\n' + ' ' * 25 + 'Total: %d' % (order-1)
        colorprint.green(msg)
        sys.exit()


def engine_register(args):
    # if the engine mode is conflicting
    if args.engine_thread and args.engine_gevent:
        colorprint.red("Cannot use Multi-Threaded mode and Coroutine mode at the same time")
        colorprint.red('Use [-eT] to set Multi-Threaded mode or [-eG] to set Coroutine mode')
        sys.exit()

    # else if engine mode is Multi-Threaded mode
    elif args.engine_thread:
        conf.engine_mode = "multi_threaded"

    # else if engine mode is Coroutine mode
    else:
        conf.engine_mode = 'coroutine'

    # set concurrent num
    if args.concurrent_num > 1000 or args.concurrent_num < 1:
        warn_msg = "setting concurrent num {}. Maybe it's too much, continue? [y/N] (default y): ".format(args.concurrent_num)
        colorprint.cyan(warn_msg, end='')
        flag = input()
        if flag.lower() in ('y', 'yes',''):
            conf.concurrent_num = args.concurrent_num
        else:
            msg = '[-] User quit!'
            colorprint.cyan(msg)
            sys.exit()
    conf.concurrent_num = args.concurrent_num


def script_register(args):

    conf.module_path = []
    # handle no scripts
    if not args.script_name:
        msg = '[-] Use -s to load script. Example: [-s spider] or [-s ./script/spider.py]'
        colorprint.red(msg)
        sys.exit()
    for script_name in args.script_name.split(","):
        # handle input: "-s ./script/spider.py"
        if os.path.split(script_name)[0]:
            if os.path.exists(script_name):
                if os.path.isfile(script_name):
                    if script_name.endswith('.py'):
                        conf.module_path.append(os.path.abspath(script_name))
                    else:
                        msg = '[-] [{}] not a Python file. Example: [-s spider] or [-s ./scripts/spider.py]' .format(script_name)
                        colorprint.red('[-] ' + msg)
                        sys.exit()
                else:
                    msg = '[-] [{}] not a file. Example: [-s spider] or [-s ./scripts/spider.py]'.format(script_name)
                    colorprint.red(msg)
                    sys.exit()
            else:
                msg = '[-] [{}] not found. Example: [-s spider] or [-s ./scripts/spider.py]'.format(script_name)
                colorprint.red(msg)
                sys.exit()

        # handle input: "-s spider"  "-s spider.py"
        else:
            if not script_name.endswith('.py'):
                script_name += '.py'
            _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, script_name))
            if os.path.isfile(_path):
                conf.module_path.append(os.path.abspath(_path))
            else:
                msg = '[-] Script [{}] not exist. Use [--show] to view all available script in ./scripts/'.format(script_name)
                colorprint.red(msg)
                sys.exit()
    # e.g. conf.module_path: ['D:\\python\\saucerframe\\scripts\\redis_unauth.py', 'D:\\python\\saucerframe\\scripts\\mongodb_unauth.py']


def target_register(args):
    
    # init target queue
    conf.target = set()

    # single target to queue
    if args.target_single:
        msg = '[+] Load target : {}'.format(args.target_single)
        colorprint.green(msg)
        conf.target.add(args.target_single)

    # file target to queue
    if args.target_file:
        if not os.path.isfile(args.target_file):
            msg = '[-] TargetFile not found: {}'.format(args.target_file)
            colorprint.red(msg)
            sys.exit()
        msg = '[+] Load targets from : {}'.format(args.target_file)
        colorprint.green(msg)
        with open(args.target_file, 'r', encoding='utf8') as f:
            targets = f.readlines()
            for target in targets:
                conf.target.add(target.strip('\n'))

    # range of ip target to queue .e.g. 192.168.1.1-192.168.1.100
    if args.target_range:
        try:
            lists = gen_ip(args.target_range)
            if (len(lists)) > 100000:
                warn_msg = "[*] Loading {} targets, Maybe it's too much, continue? [y/N]".format((len(lists)))
                colorprint.cyan(warn_msg, end='')
                flag = input()
                if flag in ('Y', 'y', 'yes', 'YES', 'Yes'):
                    pass
                else:
                    msg = '[-] User quit!'
                    colorprint.cyan(msg)
                    sys.exit()

            msg = '[+] Load targets from : {}'.format(args.target_range)
            colorprint.green(msg)

            # save to conf
            for target in lists:
                conf.target.add(target)

        except:   # Exception as e:
            # colorprint.red(e)
            err_msg = "Invalid input in [-iR], Example: -iR 192.168.1.1-192.168.1.100"
            colorprint.red(err_msg)
            sys.exit()
    
    # ip/mask e.g. 192.168.1.2/24
    if args.target_network:
        try:
            ip_range = ipaddress.ip_network(args.target_network, strict=False)
            for ip in ip_range.hosts():
                conf.target.add(ip)

        except:  #  Exception as e:
            # colorprint.red(e)
            msg = "[-] Invalid input in [-iN], Example: -iN 192.168.1.0/24"
            colorprint.red(msg)
            sys.exit()

        msg = '[+] Load targets from : {}'.format(args.target_network)
        colorprint.green(msg)

    # set search limit of api
    if args.api_limit <= 0:
        err_msg = 'Invalid input in [-limit] (can not be negative number)'
        colorprint.red(err_msg)
        sys.exit()
    if args.api_limit > 10000:
        warn_msg = "Loading {} targets, Maybe it's too much, continue? [y/N]".format(args.api_limit)
        colorprint.cyan(warn_msg)
        flag = input()
        if flag in ('Y', 'y', 'yes', 'YES', 'Yes'):
            pass
        else:
            msg = 'User quit!'
            colorprint.cyan(msg)
            sys.exit()
    conf.limit = args.api_limit

    # set search offset of api
    if args.api_offset < 0:
        warn_msg = "Wrong offset setting, would you like to set it to 0? [y/N]".format(args.api_limit)
        colorprint.cyan(warn_msg)
        flag = input()
        if flag in ('Y', 'y', 'yes', 'YES', 'Yes'):
            args.api_offset = 0
        else:
            msg = 'User quit!'
            colorprint.cyan(msg)
            sys.exit()
    conf.offset = args.api_offset

    if args.zoomeye_dork:
        from lib.api.zoomeye.zoomeye import handle_zoomeye
        # verify search_type for zoomeye
        if args.search_type not in ['web', 'host']:
            msg = '[-] Invalid value in [--search-type], show usage with [-h]'
            colorprint.red(msg)
            sys.exit()
        conf.search_type = args.search_type
        handle_zoomeye(query=args.zoomeye_dork, limit=conf.limit, type=conf.search_type, offset=conf.offset)

    if args.fofa_dork:
        from lib.api.fofa.fofa import handle_fofa
        handle_fofa(query=args.fofa_dork, limit=conf.limit, offset=conf.offset)

    if args.shodan_dork:
        from lib.api.shodan.shodan import handle_shodan
        handle_shodan(query=args.shodan_dork, limit=conf.limit, offset=conf.offset)

    if args.censys_dork:
        from lib.api.censys.censys import handle_censys
        handle_censys(query=args.censys_dork, limit=conf.limit, offset=conf.offset)

    # verify targets number
    if len(conf.target) == 0:
        err_msg = 'No targets found\nPlease load targets with [-iU|-iF|-iR|-iN] or use API with [-aZ|-aS|-aG|-aF]'
        colorprint.red(err_msg)
        sys.exit()


def output_register(args):
    # if not define output, named it by time
    if not args.output_path:
        filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt'
    else:
        filename = args.output_path
    conf.output_path = os.path.join(paths.OUTPUT_PATH, filename)
    msg = '[+] Output: %s' % conf.output_path
    colorprint.green(msg)


def proxy_regester(args):
    # if define proxy
    if args.proxy:
        proxy = args.proxy
    else:
        proxy = ConfigFileParser().proxy()
    if proxy:
        # check proxy format
        try:
            # check protocol
            protocol = proxy.split("://")[0].lower()
            if protocol not in ("socks4",'socks5','http'):
                raise Exception("proxy protocol format error, please check your proxy (socks4|socks5|http)")

            # check ip addr
            ip = proxy.split("://")[1].split(":")[0]
            compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
            if not compile_ip.match(ip):
                raise Exception("proxy ip format error, please check your proxy")

            # check port
            port = int(proxy.split("://")[1].split(":")[1])
            if not 0 <= port <= 65535:
                raise Exception("proxy port format error, please check your proxy")

        except Exception as e:
            colorprint.red(e)
            sys.exit()

        msg = "[+] setting proxy: {}://{}:{}".format(protocol, ip, port)
        colorprint.green(msg)
        conf.proxy = (protocol, ip, port)
    else:
        conf.proxy = None


def logger_lever_set(args):
    if args.logging_level == 1:
        logger.setLevel(logging.ERROR)
    elif args.logging_level == 2:
        logger.setLevel(logging.WARNING)
    elif args.logging_level == 3:
        logger.setLevel(logging.INFO)
    elif args.logging_level == 4:
        logger.setLevel(logging.DEBUG)
    elif args.logging_level == 5:
        logger.setLevel(logging.NOTSET)
    else:
        msg = 'something error when setting logger lever, please check it!'
        colorprint.red('[-] ' + msg)
        sys.exit()