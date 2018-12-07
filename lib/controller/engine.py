#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/saucer-man/saucerframe
# author = saucerman

import threading
import time
import traceback
from lib.core.data import th, conf
from lib.core.common import outputscreen
from lib.core.enums import POC_RESULT_STATUS

def initEngine():
    th.module_name = conf.Module_name # 脚本name 
    # 脚本路径？
    th.No_output_file = conf.No_output_file # 文件输出？ 
    th.output = conf.Output_file_path # 输出文件位置
    th.thread_count = th.thread_num =conf.EngineThread # # 线程数 
    # target 初始话过了，在loader中th.queue = queue.Queue()
    # 模块也找到了，th.module_obj在loader模块中<module '_' from 'D:\\saucerframe\\scripts\\test.py'>
    th.scan_count = th.found_count = 0  # 扫描数 + 找到数
    th.is_continue = True # 继续？
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
        if th.queue.qsize() > 0 and th.is_continue: # 如果queue非空，继续
            payload = str(th.queue.get(timeout=1.0)) # pop 一个 payload
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
    printProgress()
    if 'errmsg' in th:
        outputscreen.error(th.errmsg)

def resultHandler(status, payload):
    if not status or status is POC_RESULT_STATUS.FAIL:
        return
    elif status is POC_RESULT_STATUS.RETRAY:
        changeScanCount(-1) # 如果返回status是2，则将已扫描数-1；
        th.queue.put(payload) # 并且payload重新put进queue
        return
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        msg = payload # # 成功了
    else:
        msg = str(status)
    changeFoundCount(1) # 已扫描加1
    outputscreen.info(msg) # 输出屏幕
    if not th.No_output_file: # 写入文件
        output2file(msg) 

def changeScanCount(num): # 改变已经扫描的payload数+num 
    th.scan_count_lock.acquire()
    th.scan_count += num
    th.scan_count_lock.release()

def output2file(msg): # 将msg写入文件,以后要改，一次性写入
    th.file_lock.acquire()
    f = open(th.output, 'a')
    f.write(msg + '\n')
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
        th.found_count, th.queue.qsize(), th.scan_count, time.time() - th.start_time)
    # out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    outputscreen.info(msg)