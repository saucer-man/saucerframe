#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""


from lib.core.data import conf
import importlib.util
import os
import sys
import queue
from lib.core.common import colorprint


def load():
    load_poc()
    conf.task_queue = queue.Queue()
    for poc in conf.poc_module:
        for target in conf.target:
            task = {
                "poc": poc,
                "target": target
            }
            conf.task_queue.put(task)


def load_poc():
    conf.poc_module = []
    for module_path in conf.module_path:
        try:
            module_name = os.path.basename(module_path).split(".")[0]
            module_spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            # module.__name__ == module_name
            msg = '[+] Load custom script: {}'.format(os.path.basename(module_path))
            colorprint.green(msg)
            conf.poc_module.append(module)

        except Exception as e:
            msg = "[-] Your current script [{}.py] caused this exception\n{}\n{}" \
                       .format((os.path.basename(conf.module_path), '[Error Msg]: ' + str(e), \
                        'Maybe you can download this module from pip or easy_install'))
            colorprint.red(msg)
            sys.exit(0)