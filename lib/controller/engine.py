#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://xiaogeng.top)
See the file 'LICENSE' for copying permission
"""

import threading
import time
import traceback
from lib.core.data import conf,paths,th
from lib.core.common import outputscreen
from lib.core.enums import POC_RESULT_STATUS

def initEngine():
    # init control parameter
    th.result = []
    th.thread_count = th.thread_num = conf.thread_num
    th.module_name = conf.module_name
    th.module_path = conf.module_path 
    th.module_obj = conf.module_obj 
    th.target = conf.target
    th.no_output = conf.no_output 
    th.output_path = conf.output_path 
    th.scan_count = th.found_count = 0 
    th.is_continue = True 
    th.start_time = time.time() 
    setThreadLock() 
    msg = '[+] Set the number of thread: %d' % th.thread_num 
    outputscreen.success(msg) 

def setThreadLock(): 
    # set thread lock 
    th.output_screen_lock = threading.Lock()
    th.found_count_lock = threading.Lock()
    th.scan_count_lock = threading.Lock()
    th.thread_count_lock = threading.Lock()
    th.file_lock = threading.Lock() 
    th.load_lock = threading.Lock() 

def scan():
    while True:
        th.load_lock.acquire()
        if th.target.qsize() > 0 and th.is_continue: 
            payload = str(th.target.get(timeout=1.0)) 
            th.load_lock.release() 
        else:
            th.load_lock.release() 
            break
        try:
            status = th.module_obj.poc(payload) 
            resultHandler(status, payload) 
        except Exception:
            th.errmsg = traceback.format_exc()
            th.is_continue = False
        # set scanned count + 1
        changeScanCount(1) 
    # set running thread -1
    changeThreadCount(-1) # 

def run():
    initEngine()
    for i in range(th.thread_num): 
        t = threading.Thread(target=scan, name=str(i))
        t.setDaemon(True)
        t.start()
    # It can quit with Ctrl-C
    while 1:
        if th.thread_count > 0 and th.is_continue:
            time.sleep(0.01)
        else:
            break
    # save result to output file
    if not th.no_output:
        output2file(th.result) 
    printProgress()
    if 'errmsg' in th:
        outputscreen.error(th.errmsg)

def resultHandler(status, payload):
    # if no vulnerable
    if not status or status is POC_RESULT_STATUS.FAIL:
        # msg = '[-] ' + payload
        # outputscreen.info(msg)
        return 
    # try again 
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1) 
        th.target.put(payload) 
        return
    # vulnerable
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = '[+] ' + payload
        th.output_screen_lock.acquire()
        outputscreen.info(msg) # 成功了
        th.output_screen_lock.release()
    else:
        msg = str(status)
        outputscreen.warning(msg)
    # get found number of payload +1
    changeFoundCount(1) 

    th.result.append(msg)

    # if result list is too large, save it to file and empty list
    if len(th.result) > 5000:
        if not th.no_output:
            output2file(th.result) 
            th.result = []

def changeScanCount(num): 
    th.scan_count_lock.acquire()
    th.scan_count += num
    th.scan_count_lock.release()

def output2file(msg): 
    th.file_lock.acquire()
    f = open(th.output_path, 'a')
    for res in msg:
        f.write(res + '\n')
    f.close()
    th.file_lock.release()

def changeFoundCount(num):
    th.found_count_lock.acquire()
    th.found_count += num
    th.found_count_lock.release()

def changeThreadCount(num): 
    th.thread_count_lock.acquire()
    th.thread_count += num
    th.thread_count_lock.release()

def printProgress(): 
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        th.found_count, th.target.qsize(), th.scan_count, time.time() - th.start_time)
    # out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    outputscreen.blue(msg)