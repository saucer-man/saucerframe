#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/saucer-man/saucerframe
# author = saucerman

import os
from lib.parse.cmdline import cmdLineParser
from lib.core.common import outputscreen, setpaths
from lib.core.data import paths, conf, cmdLineOptions
from lib.core.option import initOptions
# from lib.controller.loader import loadModule, loadPayloads
from lib.controller.engine import run

def main():
    """
    main fuction of saucerframe 
    """
    paths.ROOT_PATH = os.getcwd() # 获取root_path D:\saucerframe
    setpaths() # 设置路径
    cmdLineOptions.update(cmdLineParser().__dict__) # cmdLineOptions接收参数
    #{'thread_num': 10, 'script_name': '', 'target_single': 'fdsafd', 'target_file': '', 'output_file': '', 'output_file_status': True}
    outputscreen.banner() # 输出脚本

    
    initOptions(cmdLineOptions) # 设置了一下参数给conf

    
    #loadModule() # 验证script是否有poc模块，加载module
    #loadPayloads() # 将payload目标加载进th.payload

    # run() # 运行engine


if __name__ == "__main__":
    main()
