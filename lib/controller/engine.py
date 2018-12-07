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
    th.result = []
    th.thread_count = th.thread_num = conf.thread_num # 线程
    th.module_name = conf.module_name #  test.py
    th.module_path = conf.module_path #  D:\saucerframe\scripts\test.py
    th.module_obj = conf.module_obj # POC
    th.target = conf.target # target queue
    th.no_output = conf.no_output # True /False
    th.output_path = conf.output_path # D:\saucerframe\output\2018-12-02 22:30:26.txt
    th.scan_count = th.found_count = 0  # 已经扫描数 + 已经找到数
    th.is_continue = True # 继续？控制参数
    th.start_time = time.time() # 开始时间 
    setThreadLock() # 线程锁初始话，下面--》
    msg = 'Set the number of concurrent: %d' % th.thread_num # 线程数
    outputscreen.success(msg) 

def setThreadLock(): # 生成锁对象，全局唯一
    th.found_count_lock = threading.Lock() # 找到数目锁
    th.scan_count_lock = threading.Lock() # 扫描数目锁
    th.thread_count_lock = threading.Lock() # 线程过程锁
    th.file_lock = threading.Lock() # 文件锁
    th.load_lock = threading.Lock() # 加载锁

def scan():
    while True:
        th.load_lock.acquire()# 则加载线程锁
        if th.target.qsize() > 0 and th.is_continue: # 如果queue非空，继续
            payload = str(th.target.get(timeout=1.0)) # pop 一个 payload
            th.load_lock.release() # 释放线程锁
        else:
            th.load_lock.release() # 释放线程锁
            break
        try:
            # POC在执行时报错如果不被处理，线程框架会停止并退出
            status = th.module_obj.poc(payload) # payload加载进module
            resultHandler(status, payload) 
        except Exception:
            th.errmsg = traceback.format_exc()
            th.is_continue = False
        changeScanCount(1) # 已扫描的payload+1
    changeThreadCount(-1) # 正在进行的进程数-1

def run():
    initEngine() # th参数设置
    for i in range(th.thread_num): # 创建多线程 
        t = threading.Thread(target=scan, name=str(i))
        t.setDaemon(True)
        t.start()
    # It can quit with Ctrl-C
    while 1:
        if th.thread_count > 0 and th.is_continue:
            time.sleep(0.01)
        else:
            break
    if not th.no_output: # 写入文件
        output2file(th.result) 
    printProgress()
    if 'errmsg' in th:
        outputscreen.error(th.errmsg)

def resultHandler(status, payload):
    if not status or status is POC_RESULT_STATUS.FAIL:
        msg = '[-] ' + payload
        outputscreen.success(msg) # 没找到
        return 
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1) # 如果返回status是2，则将已扫描数-1；
        th.target.put(payload) # 并且payload重新put进queue
        return
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = '[+] ' + payload
        outputscreen.success(msg) # 成功了
    else:
        msg = str(status)
        outputscreen.warning(msg)
    changeFoundCount(1) # 成功找的的payload加1
    th.result.append(msg)
    if len(th.result) > 1000:
        if not th.no_output: # 写入文件
            output2file(th.result) 
            th.result = []

def changeScanCount(num): # 改变已经扫描的payload数+num 
    th.scan_count_lock.acquire()
    th.scan_count += num
    th.scan_count_lock.release()

def output2file(msg): # 将msg列表写入文件
    th.file_lock.acquire()
    f = open(th.output_path, 'a')
    for res in msg:
        f.write(res + '\n')
    f.close()
    th.file_lock.release()

def changeFoundCount(num): # 改变找到目标的数目
    th.found_count_lock.acquire()
    th.found_count += num
    th.found_count_lock.release()

def changeThreadCount(num): # 改变正在扫描的线程数
    th.thread_count_lock.acquire()
    th.thread_count += num
    th.thread_count_lock.release()

def printProgress(): # 输出状态
    msg = '%s found | %s remaining | %s scanned in %.2f seconds' % (
        th.found_count, th.target.qsize(), th.scan_count, time.time() - th.start_time)
    # out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    outputscreen.info(msg)