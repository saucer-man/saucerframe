#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
import queue
import logging
import os
import sys
import time
import ipaddress
from lib.core.data import paths, conf, logger
from lib.core.common import colorprint, gen_ip
from lib.api.zoomeye.zoomeye import handle_zoomeye
from lib.api.fofa.fofa import handle_fofa
from lib.api.shodan.shodan import handle_shodan
from lib.api.google.google import handle_google
from lib.api.censys.censys import handle_censys

def init_options(args):
    check_show(args)
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
            if module not in ['__init__.py','test.py'] and os.path.splitext(module)[1] == '.py':
                colorprint.green(str(order)+ '. ' +module)
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
        # set threads num
        if args.thread_num > 200 or args.thread_num < 1:
            msg = '[*] Invalid input in [-t](range: 1 to 200), has changed to default(30)'
            colorprint.cyan(msg)
            conf.thread_num = 30
            return 
        conf.thread_num = args.thread_num

    # else if engine mode is Coroutine mode
    else:
        conf.engine_mode = 'coroutine'


def script_register(args):

    # handle no scripts
    if not args.script_name:
        msg = '[-] Use -s to load script. Example: [-s spider] or [-s ./script/spider.py]'
        colorprint.red(msg)
        sys.exit()

    # handle input: "-s ./script/spider.py"
    if os.path.split(args.script_name)[0]:
        if os.path.exists(args.script_name):
            if os.path.isfile(args.script_name):
                if args.script_name.endswith('.py'):
                    conf.module_path = os.path.abspath(args.script_name)
                else:
                    msg = '[-] [%s] not a Python file. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
                    colorprint.red('[-] ' + msg)
                    sys.exit()
            else:
                msg = '[-] [%s] not a file. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
                colorprint.red(msg)
                sys.exit()
        else:
            msg = '[-] [%s] not found. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
            colorprint.red(msg)
            sys.exit()

    # handle input: "-s spider"  "-s spider.py"
    else:
        if not args.script_name.endswith('.py'):
            args.script_name += '.py'
        _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, args.script_name))
        if os.path.isfile(_path):
            conf.module_path = os.path.abspath(_path)
        else:
            msg = '[-] Script [%s] not exist. Use [--show] to view all available script in ./scripts/' % args.script_name
            colorprint.red(msg)
            sys.exit()
    # conf.module_path: D:\software\tools\saucerframe\scripts\test.py


def target_register(args):
    msg = '[*] Initialize targets...'
    colorprint.cyan(msg)
    
    # init target queue
    conf.target = queue.Queue()

    # single target to queue
    if args.target_single:
        msg = '[+] Load target : %s' % args.target_single
        colorprint.green(msg)
        conf.target.put(args.target_single)

    # file target to queue
    elif args.target_file:
        if not os.path.isfile(args.target_file):
            msg = '[-] TargetFile not found: %s' % args.target_file
            colorprint.red(msg)
            sys.exit()
        msg = '[+] Load targets from : %s' % args.target_file
        colorprint.green(msg)
        with open(args.target_file, 'r', encoding='utf8') as f:
            targets = f.readlines()
            for target in targets:
                conf.target.put(target.strip('\n'))

    # range of ip target to queue .e.g. 192.168.1.1-192.168.1.100
    elif args.target_range:
        try:
            lists = gen_ip(args.target_range)
            if (len(lists)) > 100000:
                warn_msg = "[*] Loading %d targets, Maybe it's too much, continue? [y/N]" % (len(lists))
                colorprint.cyan(warn_msg)
                flag = input()
                if flag in ('Y', 'y', 'yes', 'YES','Yes'):
                    pass
                else:
                    msg = '[-] User quit!'
                    colorprint.cyan(msg)
                    sys.exit()
            
            msg = '[+] Load targets from : %s' % args.target_range
            colorprint.green(msg)

            # save to conf
            for target in lists:
                conf.target.put(target)
        except Exception as e:
            # colorprint.red(e)
            err_msg = "Invalid input in [-iR], Example: -iR 192.168.1.1-192.168.1.100"
            colorprint.red(err_msg)
            sys.exit()
    
    # ip/mask e.g. 192.168.1.2/24
    elif args.target_network:
        try:
            ip_range = ipaddress.ip_network(args.target_network, strict=False)
            for ip in ip_range.hosts():
                conf.target.put(ip)

        except Exception as e:
            # colorprint.red(e)
            msg = "[-] Invalid input in [-iN], Example: -iN 192.168.1.0/24"
            colorprint.red(msg)
            sys.exit()

        msg = '[+] Load targets from : %s' % args.target_network
        colorprint.green(msg)

    else:
        # set search limit of api
        if args.api_limit <= 0:
            err_msg = 'Invalid input in [-limit] (can not be negative number)'
            colorprint.red(err_msg)
            sys.exit()
        elif args.api_limit > 10000:
            warn_msg = "Loading {} targets, Maybe it's too much, continue? [y/N]".format(args.api_limit)
            colorprint.cyan(warn_msg)
            flag = input()
            if flag in ('Y', 'y', 'yes', 'YES','Yes'):
                pass
            else:
                msg = 'User quit!'
                colorprint.cyan(msg)
                sys.exit()
        conf.limit = args.api_limit
        
        # set search offset of api
        conf.offset = args.api_offset

        if args.zoomeye_dork:
            # verify search_type for zoomeye
            if args.search_type not in ['web', 'host']:
                msg = '[-] Invalid value in [--search-type], show usage with [-h]'
                colorprint.red(msg)
                sys.exit()
            conf.search_type = args.search_type
            handle_zoomeye(query=args.zoomeye_dork, limit=conf.limit, type=conf.search_type, offset = conf.offset)

        elif args.fofa_dork:
            handle_fofa(query=args.fofa_dork, limit=conf.limit, offset=conf.offset)
        
        elif args.shodan_dork:
            handle_shodan(query=args.shodan_dork, limit=conf.limit, offset=conf.offset)

        elif args.censys_dork:
            handle_censys(query=args.censys_dork, limit=conf.limit, offset=conf.offset)

        elif args.google_dork:
            conf.google_proxy = args.google_proxy
            handle_google(query=args.google_dork, limit = conf.limit, offset=conf.offset)

    # verify targets number
    if conf.target.qsize() == 0:
        err_msg = 'No targets found\nPlease load targets with [-iU|-iF|-iR|-iN] or use API with [-aZ|-aS|-aG|-aF]'
        colorprint.red(err_msg)
        sys.exit()

def output_register(args):

    # if not define output, named it by time
    if not args.output_path:
        filename = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.txt'

    conf.output_path = os.path.join(paths.OUTPUT_PATH, filename)
    msg = '[+] Output: %s' % conf.output_path
    colorprint.green(msg)
    if args.logging_level >= 1:
        logger.setLevel(logging.DEBUG)




