#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/saucer-man/saucerframe
# author = saucerman
'''
验证script是否有poc模块
讲payload目标加载进th.payload
'''

import queue
import imp
import os
import sys
from lib.core.data import conf, th, paths
from lib.core.common import outputscreen
from lib.core.setting import ESSENTIAL_MODULE_METHODS


def loadModule(): # 加载script
    _name = conf.Module_name
    msg = 'Load custom script: %s' % _name
    outputscreen.success(msg)

    fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
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
        th.module_obj = imp.load_module("_", fp, pathname, description) # <module '_' from 'D:\\saucerframe\\scripts\\test.py'>
        for each in ESSENTIAL_MODULE_METHODS: # each ='poc'
            if not hasattr(th.module_obj, each): # module_obj dot hasattr 'poc' module
                errorMsg = "Can't find essential method:'%s' in current script，Please modify your script." % each
                outputscreen.error(errorMsg)
                sys.exit(0)
    except ImportError as e:
        errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
                   % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        outputscreen.error(errorMsg)
        sys.exit(0)

def loadPayloads():
    infoMsg = 'Initialize targets...'
    outputscreen.success(infoMsg)
    th.queue = queue.Queue()
    # if conf.TARGET_MODE is TARGET_MODE_STATUS.RANGE:
    #     int_mode()
    # elif conf.TARGET_MODE is TARGET_MODE_STATUS.FILE:
    #     file_mode()
    # elif conf.TARGET_MODE is TARGET_MODE_STATUS.IPMASK:
    #     net_mode()
    # elif conf.TARGET_MODE is TARGET_MODE_STATUS.SINGLE:
    #     single_target_mode()
    # elif conf.TARGET_MODE is TARGET_MODE_STATUS.API:
    #     api_mode()
    for payload in conf.Target:
        th.queue.put(payload)