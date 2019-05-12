#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

import gevent
import sys
import threading
import time
import os
import traceback
import importlib.util
from lib.core.setting import ESSENTIAL_MODULE_METHODS
from lib.core.data import conf, th, logger
from lib.core.common import colorprint
from lib.core.enums import POC_RESULT_STATUS
from lib.utils.console import getTerminalSize


def initEngine():
    # load module
    load_module()
    # init control parameter
    th.result = []
    th.thread_mode = True if conf.engine_mode == "multi_threaded" else False
    th.target = conf.target
    th.output_path = conf.output_path 
    th.scan_count = th.found_count = 0 
    th.is_continue = True 
    th.console_width = getTerminalSize()[0] - 2
    # set concurrent number
    if th.thread_mode:
        th.concurrent_count = th.concurrent_num = conf.thread_num
    else:
        if th.target.qsize() < 150:
            th.concurrent_count = th.concurrent_num = th.target.qsize()
        else:
            th.concurrent_count = th.concurrent_num = 150
    th.start_time = time.time()


def load_module():
    global scan_module
    try:
        module_spec = importlib.util.spec_from_file_location(ESSENTIAL_MODULE_METHODS, conf.module_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        # bug here how to change poc-->ESSENTIAL_MODULE_METHODS
        scan_module = module.poc

        msg = '[+] Load custom script: %s' % os.path.basename(conf.module_path)
        colorprint.green(msg)

    except Exception as e:
        msg = "[-] Your current script [%s.py] caused this exception\n%s\n%s" \
                   % (os.path.basename(conf.module_path), '[Error Msg]: ' + str(e),\
                      'Maybe you can download this module from pip or easy_install')
        colorprint.red(msg)
        sys.exit(0)


def setThreadLock(): 
    # set thread lock 
    th.output_screen_lock = threading.Lock()
    th.found_count_lock = threading.Lock()
    th.scan_count_lock = threading.Lock()
    th.concurrent_count_lock = threading.Lock()
    th.file_lock = threading.Lock() 
    th.load_lock = threading.Lock() 


def scan():
    while True:
        if th.thread_mode: th.load_lock.acquire()
        if th.target.qsize() > 0 and th.is_continue: 
            payload = str(th.target.get(timeout=1.0))
            logger.debug("testing:"+payload)
            sys.stdout.write(payload + " " * (th.console_width - len(payload)) + "\r")
            sys.stdout.flush()
            if th.thread_mode: th.load_lock.release()
        else:
            if th.thread_mode: th.load_lock.release()
            break
        try:
            status = scan_module(payload)
            resultHandler(status, payload) 
        except Exception as e:
            th.err_msg = traceback.format_exc()
            th.is_continue = False
        # set scanned count + 1
        change_scan_count(1) 
    # set running concurrent count -1
    change_concurrent_count(-1) # 


def run():
    initEngine()
    if th.thread_mode:
        # set lock for multi_threaded mode   
        setThreadLock() 
        colorprint.green('[+] Set working way Multi-Threaded mode')
        colorprint.green('[+] Set the number of thread: %d' % th.concurrent_num) 
        for i in range(th.concurrent_num): 
            t = threading.Thread(target=scan, name=str(i))
            t.setDaemon(True)
            t.start()
        # It can quit with Ctrl-C
        while th.concurrent_count > 0 and th.is_continue:
                time.sleep(0.01)

    # Coroutine mode
    else:
        colorprint.green('[+] Set working way Coroutine mode')
        colorprint.green('[+] Set the number of Coroutine: %d' % th.concurrent_num) 
        gevent.joinall([gevent.spawn(scan) for i in range(0, th.concurrent_num)])

    # save result to output file

    output2file(th.result)
    printProgress()
    if 'err_msg' in th:
        colorprint.red(th.err_msg)


def resultHandler(status, payload):

    if not status or status is POC_RESULT_STATUS.FAIL:
        return

    # try again 
    elif status is POC_RESULT_STATUS.RETRAY:
        change_scan_count(-1) 
        th.target.put(payload) 
        return

    # vulnerable
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = '[+] ' + payload
        if th.thread_mode: th.output_screen_lock.acquire()
        colorprint.white(msg)
        if th.thread_mode: th.output_screen_lock.release()
        th.result.append(payload)

    # If there is a lot of information, Line feed display
    elif isinstance(status, list):
        if th.thread_mode: th.output_screen_lock.acquire()
        for msg in status:
            colorprint.white(msg)
            th.result.append(msg)
        if th.thread_mode: th.output_screen_lock.release()
        
    else:
        msg = str(status)
        if th.thread_mode: th.output_screen_lock.acquire()
        colorprint.white(msg)
        if th.thread_mode: th.output_screen_lock.release()
        th.result.append(msg)

    # get found number of payload +1
    change_found_count(1) 

    # if result list is too large, save it to file and empty list
    if len(th.result) > 5000:
        output2file(th.result)
        th.result = []


def change_scan_count(num): 
    if th.thread_mode: th.scan_count_lock.acquire()
    th.scan_count += num
    if th.thread_mode: th.scan_count_lock.release()


def output2file(msg): 
    if th.thread_mode: th.file_lock.acquire()
    with open(th.output_path, 'a') as f:
        for res in msg:
            f.write(res + '\n')
    if th.thread_mode: th.file_lock.release()


def change_found_count(num):
    if th.thread_mode: th.found_count_lock.acquire()
    th.found_count += num
    if th.thread_mode: th.found_count_lock.release()


def change_concurrent_count(num): 
    if th.thread_mode: th.concurrent_count_lock.acquire()
    th.concurrent_count += num
    if th.thread_mode: th.concurrent_count_lock.release()


def printProgress(): 
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        th.found_count, th.target.qsize(), th.scan_count, time.time() - th.start_time)
    out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    colorprint.blue(out)