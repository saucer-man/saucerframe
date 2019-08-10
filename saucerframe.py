#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from gevent import monkey
monkey.patch_all()
from lib.parse.cmdline import cmdLineParser
from lib.core.common import colorprint, set_paths, banner
from lib.core.data import cmdLineOptions
from lib.core.option import init_options
from lib.controller.engine import run
from lib.controller.loader import load
import os
import time
import sys
import traceback

def module_path():
    """
    This will get us the program's directory
    """
    return os.path.dirname(os.path.realpath(__file__))


def check_environment():
    try:
        os.path.isdir(module_path())
    except Exception:
        err_msg = "your system does not properly handle non-ASCII paths. "
        err_msg += "Please move the pocsuite's directory to the other location"
        colorprint.red(err_msg)
        raise SystemExit


def check_python_version():
    if sys.version_info < (3, 4):
        sys.exit("Python {}.{} or later is required.\n".format(3, 4))


def main():
    try:
        check_python_version()
        check_environment()

        # set paths of project
        set_paths(module_path())

        # output banner information
        banner() 

        # received command >> cmdLineOptions
        cmdLineOptions.update(cmdLineParser().__dict__)

        # loader script,target,working way(threads? gevent?),output_file from cmdLineOptions
        # and send it to conf
        init_options(cmdLineOptions)

        # load poc module and target --> tasks
        load()

        # run!
        run()
    except Exception as e:
        print(e)

    finally:
        print("\n\n[*] shutting down at {0}\n".format(time.strftime("%X")))


if __name__ == "__main__":
    main()
