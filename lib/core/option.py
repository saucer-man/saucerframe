#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/saucer-man/saucerframe
# author = saucerman

"""
conf.thread_num 线程 10
conf.module_name 脚本名 test.py
conf.module_path 脚本路径 D:\saucerframe\scripts\test.py
conf.module_obj 脚本中的poc模块
conf.target 目标queue（未做验证） ['www.xiaogeng.top', 'www.xiaogeng.top','hello']

conf.no_output 不输出？默认false----True /False
conf.output_path 输出位置 D:\saucerframe\output\2018-12-02 22:30:26.txt
"""
from thirdparty.IPy.IPy import IP
import queue
import os
import sys
import imp
import time
from lib.core.data import paths, conf
from lib.core.common import outputscreen, gen_ip
from lib.core.setting import ESSENTIAL_MODULE_METHODS
from lib.api.zoomeye.zoomeye import handle_zoomeye

def initOptions(args):
    checkShow(args) # 是否需要show script
    EngineRegister(args) # 线程注册（设置线程）
    ScriptRegister(args) # 加载脚本注册
    TargetRegister(args) # 目标注册
    Output(args) # 输出文件注册



def checkShow(args):
    # 如果show，则show一下
    if args.show_scripts:
        module_name_list = os.listdir(paths.SCRIPT_PATH)
        #print(module_name_list)
        outputscreen.info('Script Name (total:%s)\n' % str(len(module_name_list) - 1))
        for module in module_name_list:
            outputscreen.info(module)
        sys.exit()


def EngineRegister(args):
    if args.thread_num > 100 or args.thread_num < 1:
        # msg = 'Invalid input in [-t], range: 1 to 100, has changed to default(10)'
        # outputscreen.error(msg)
        conf.thread_num = 10
    conf.thread_num = args.thread_num

def ScriptRegister(args):

    # 如果指定脚本
    if not args.script_name:
        msg = 'Use -s to load script. Example: [-s spider] or [-s ./script/spider.py]'
        outputscreen.error(msg)
        sys.exit()

    # handle input: "-s ./script/spider.py"
    if os.path.split(args.script_name)[0]:
        if os.path.exists(args.script_name):
            if os.path.isfile(args.script_name):
                if args.script_name.endswith('.py'):
                    conf.module_name = os.path.split(args.script_name)[-1]
                    conf.module_path = os.path.abspath(args.script_name)
                else:
                    msg = '[%s] not a Python file. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
                    outputscreen.error(msg)
                    sys.exit()
            else:
                msg = '[%s] not a file. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
                outputscreen.error(msg)
                sys.exit()
        else:
            msg = '[%s] not found. Example: [-s spider] or [-s ./scripts/spider.py]' % args.script_name
            outputscreen.error(msg)
            sys.exit()

    # handle input: "-s spider"  "-s spider.py"
    else:
        if not args.script_name.endswith('.py'):
            args.script_name += '.py'
        _path = os.path.abspath(os.path.join(paths.SCRIPT_PATH, args.script_name))
        if os.path.isfile(_path):
            conf.module_name = args.script_name
            conf.module_path = os.path.abspath(_path)
        else:
            msg = 'Script [%s] not exist. Use [--show] to view all available script in ./scripts/' % args.script_name
            outputscreen.error(msg)
            sys.exit()
    # outputscreen.info(conf.Module_name) # test.py
    # outputscreen.info(conf.Module_file_path) #  D:\saucerframe\scripts\test.py

    # 接下来加载module到conf.module_obj
    msg = 'Load custom script: %s' % conf.module_name
    outputscreen.success(msg)

    fp, pathname, description = imp.find_module(os.path.splitext(conf.module_name)[0], [paths.SCRIPT_PATH])
    '''
    >>> fp, pathname, description = imp.find_module('test',['D:\saucerframe\scripts'])
    >>> fp
        _io.TextIOWrapper name='D:\\saucerframe\\scripts\\test.py' mode='r' encoding='utf-8'>
    >>> pathname
        'D:\\saucerframe\\scripts\\test.py'
    >>> description
        ('.py', 'r', 1)
    '''
    try:
        conf.module_obj = imp.load_module("_", fp, pathname, description) # <module '_' from 'D:\\saucerframe\\scripts\\test.py'>
        for each in ESSENTIAL_MODULE_METHODS: # each ='poc'
            if not hasattr(conf.module_obj, each): # module_obj dot hasattr 'poc' module
                errorMsg = "Can't find essential method:'%s' in current script，Please modify your script." % each
                outputscreen.error(errorMsg)
                sys.exit(0)
    except ImportError as e:
        errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
                   % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        outputscreen.error(errorMsg)
        sys.exit(0)

def TargetRegister(args):
    infoMsg = 'Initialize targets...'
    outputscreen.success(infoMsg)
    
    # 设置一下api limit
    conf.target = queue.Queue()

    # 单个目标>queue
    if args.target_single:
        conf.target.put(args.target_single)

    # 文件目标  e.g. D:/target.txt
    elif args.target_file:
        if not os.path.isfile(args.target_file):
            msg = 'TargetFile not found: %s' % args.target_file
            outputscreen.error(msg)
            sys.exit()

        with open(args.target_file, 'r', encoding='utf8') as f:
            targets = f.readlines()
            for target in targets:
                conf.target.put(target.strip('\n'))
    # 随机生成
    elif args.target_range:
        try:
            lists = gen_ip(args.target_range)
            if (len(lists))>100000:
                warnmsg = "Loading %d targets, Maybe it's too much, continue? [y/N]" % (len(lists))
                outputscreen.warning(warnmsg)
                flag =input()
                if a in ('Y', 'y', 'yes', 'YES','Yes'):
                    pass
                else:
                    msg = 'User quit!'
                    outputscreen.warning(msg)
                    sys.exit()
            # save to conf
            for target in lists:
                conf.target.put(target)
        except:
            helpmsg = "Invalid input in [-iR], Example: -iR 192.168.1.1-192.168.1.100"
            outputscreen.error(helpmsg)
            sys.exit()
    
    # 网络+子网掩码
    elif args.target_network: # 192.168.1.2/24
        try:
            # 根据掩码算出子网掩码24--》255.255.255.0
            ip_format= args.target_network.split('/')# ['192.168.1.2', '24']
            ip_str = IP(ip_format[0]).strBin() # 11000000101010000000000100000010
            ip_str = ip_str[0:int(ip_format[1])]+'0'*(32-int(ip_format[1])) # '11000000101010000000000100000000'
            ip = "%s.%s.%s.%s"%(str(int(ip_str[0:8],2)), str(int(ip_str[8:16],2)), str(int(ip_str[16:24],2)), str(int(ip_str[24:32],2)))
            #print(ip)
            # 192.168.1.0
            ip_range = IP('%s/%s'%(ip,ip_format[1]))
            #print(ip_range)
            for i in ip_range:
                conf.target.put(i)
        except:
            helpmsg = "Invalid input in [-iN], Example: -iN 192.168.1.0/24"
            outputscreen.error(helpmsg)
            sys.exit()
            
    else:
        # 如果都不是则就是调用了api,首先设置一下limit
        if args.api_limit <= 0:
            errormsg = 'Invalid input in [-limit] (can not be negative number)'
            outputscreen.error(errormsg)
            sys.exit()
        elif args.api_limit>100000:
            warnmsg = "Loading %d targets, Maybe it's too much, continue? [y/N]" % (len(lists))
            outputscreen.warning(warnmsg)
            flag =input()
            if a in ('Y', 'y', 'yes', 'YES','Yes'):
                pass
            else:
                msg = 'User quit!'
                outputscreen.warning(msg)
                sys.exit()
        conf.limit = args.api_limit
        
        conf.offset = args.api_offset

        if args.zoomeye_dork:
            # 如果是钟馗之眼还需要设置search_type
            if args.search_type not in ['web', 'host']:
                msg = 'Invalid value in [--search-type], show usage with [-h]'
                outputscreen.error(msg)
                sys.exit()
            conf.search_type = args.search_type
            handle_zoomeye(query = args.zoomeye_dork, limit = conf.limit, type = conf.search_type, offset = conf.offset)

        elif args.fofa_dork:
            handle_fofa(query= args.fofa_dork, limit=conf.limit, offset = conf.offset)
        
        elif args.shodan_dork:
            handle_shodan(args.shodan_dork)


        # elif args.google_dork:
        #     conf.google_proxy = google_proxy
        #     handle_google(args.google_dork)

    if conf.target.qsize() == 0:
        errormsg = msg = 'No targets found\nPlease load targets with [-iU|-iF|-iR|-iN] or use API with [-aZ|-aS|-aG|-aF]'
        outputscreen.error(errormsg)
        sys.exit()

    while conf.target.qsize() >0:
        a = conf.target.get()
        print(a,end='  ')
            

        



def Output(args):
    if args.no_output and args.output_path:
        msg = 'Cannot use [-oF] and [-o] together, please read the usage with [-h].'
        outputscreen.error(msg)
        sys.exit()

    conf.no_output = args.no_output 
    
    if not args.no_output:
        # not define output_path, default named by time
        if not args.output_path:
            filename= time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +'.txt'
            #msg = 'not define output_filename, default named by time(%s)' % output_filename
            #outputscreen.warning(msg)
        
        conf.output_path = os.path.join(paths.OUTPUT_PATH, filename)




