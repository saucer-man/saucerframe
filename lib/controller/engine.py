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
import traceback
from lib.core.data import conf, th
from lib.core.common import colorprint
from lib.core.enums import POC_RESULT_STATUS
from lib.utils.console import getTerminalSize
from lib.core.log import logger


def init_engine():
    # init control parameter
    th.result = []
    th.thread_mode = True if conf.engine_mode == "multi_threaded" else False
    th.tasks = conf.task_queue
    th.tasks_num = conf.task_queue.qsize()
    th.output_path = conf.output_path 
    th.scan_count = th.found_count = 0 
    th.is_continue = True 
    th.console_width = getTerminalSize()[0] - 2

    # set concurrent number
    if th.tasks.qsize() < conf.concurrent_num:
        th.concurrent_count = th.concurrent_num = th.tasks.qsize()
    else:
        th.concurrent_count = th.concurrent_num = conf.concurrent_num
    
    th.start_time = time.time()


def set_threadLock():
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
        if th.tasks.qsize() > 0 and th.is_continue:
            task = th.tasks.get(timeout=1.0)
            payload = str(task["target"])
            module_obj = task["poc"]
            sys.stdout.write("(" + str(th.tasks_num-th.tasks.qsize()) + "/" + str(th.tasks_num) + ")\r")
            sys.stdout.flush()
            logger.info("testing: [{}] {}".format(module_obj.__name__, payload))
            # colorprint.white(payload, end = '\r', flush=True) --> useless because of slow
            if th.thread_mode: th.load_lock.release()
        else:
            if th.thread_mode: th.load_lock.release()
            break
        try:
            status = module_obj.poc(payload)
            result_handler(status, task)
        except:
            th.err_msg = traceback.format_exc()
            th.is_continue = False
        # set scanned count + 1
        change_scan_count(1) 
    # set running concurrent count -1
    change_concurrent_count(-1) # 


def free_conf_memory():
    for k in conf.keys():
        conf[k] = None


def run():
    init_engine()
    free_conf_memory()
    if th.thread_mode:
        # set lock for multi_threaded mode   
        set_threadLock()
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
    print_progress()
    if 'err_msg' in th:
        colorprint.red(th.err_msg)


def result_handler(status, task):
    if not status or status is POC_RESULT_STATUS.FAIL:
        logger.debug('not vuln: [{}] {}'.format(task['poc'].__name__, task["target"]))
        return

    # try again 
    elif status is POC_RESULT_STATUS.RETRAY:
        logger.debug('try again: [{}] {}'.format(task['poc'].__name__, task["target"]))
        change_scan_count(-1)
        th.tasks.put(task)
        return

    # vulnerable
    elif status is True or status is POC_RESULT_STATUS.SUCCESS:
        logger.debug('vuln: [{}] {}'.format(task['poc'].__name__, task["target"]))
        msg = '[{}] {}'.format(task['poc'].__name__, task["target"])
        if th.thread_mode: th.output_screen_lock.acquire()
        colorprint.white(msg + " " * (th.console_width - len(msg)))
        if th.thread_mode: th.output_screen_lock.release()
        th.result.append(msg)

    # If there is a lot of information, Line feed display
    elif isinstance(status, list):
        if th.thread_mode: th.output_screen_lock.acquire()
        for _msg in status:
            msg = '[{}] {}'.format(task['poc'].__name__, _msg)
            colorprint.white(msg + " " * (th.console_width - len(msg)))
            th.result.append(msg)
        if th.thread_mode: th.output_screen_lock.release()
        
    else:
        msg = '[{}] {}'.format(task['poc'].__name__, str(status))
        if th.thread_mode: th.output_screen_lock.acquire()
        colorprint.white(msg + " " * (th.console_width - len(msg)))
        if th.thread_mode: th.output_screen_lock.release()
        th.result.append(msg)

    # get found number of payload +1
    change_found_count(1) 

    # save result to file and empty list
    if th.result:
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


def print_progress():
    print('\n')
    msg = '%s found | %s remaining | %s tasks done in %.2f seconds' % (
        th.found_count, th.tasks.qsize(), th.scan_count, time.time() - th.start_time)
    out = '\r' + ' ' * (th.console_width - len(msg)) + msg
    colorprint.blue(out)