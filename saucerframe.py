#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""

from gevent import monkey
monkey.patch_all()
import os
from lib.parse.cmdline import cmdLineParser
from lib.core.common import outputscreen, setpaths, banner
from lib.core.data import paths, conf, cmdLineOptions
from lib.core.option import initOptions
from lib.controller.engine import run

def main():
    """
    main fuction of saucerframe 
    """

    # anyway output thr banner information
    banner() 
    
    # set paths of project 
    paths.ROOT_PATH = os.getcwd() 
    setpaths()
    
    # received command >> cmdLineOptions
    cmdLineOptions.update(cmdLineParser().__dict__)
    
    # loader script,target,working way(threads? gevent?),output_file from cmdLineOptions
    # and send it to conf
    initOptions(cmdLineOptions) 

    # run!
    run()

if __name__ == "__main__":
    main()
