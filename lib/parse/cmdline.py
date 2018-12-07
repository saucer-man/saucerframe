#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# project = https://github.com/saucer-man/saucerframe
# author = saucerman

import sys
import argparse

def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    """
    parser = argparse.ArgumentParser(usage='python saucerframe-T.py -s bingc -aZ "port:8080"')
    
    # engine
    engine = parser.add_argument_group("Engine", "Decide the threads of engine")
    engine.add_argument("-t","--thread",  dest="thread_num", type=int, default=10,
                        help="num of threads, 10 by default")
    
    # script
    script = parser.add_argument_group("Script", "Choice script you want to use")
    script.add_argument("-s", "--script",  dest="script_name", type=str, default="",
                        help="load script by name (-s jboss-rce)")
    script.add_argument('--show', dest="show_scripts", default=False, action='store_true',
                      help='show available script names in ./script/ and exit')    
    # target               
    target = parser.add_argument_group("Target","At least one of these options"
                                          "has to be provided to define the target(s)")
    target.add_argument("-iU", metavar='TARGET', dest="target_single", type=str, default="",
                        help="scan a single target (e.g. www.wooyun.org)")
    target.add_argument("-iF", metavar='FILE', dest="target_file", type=str, default="",
                        help="load targets from targetFile (e.g. wooyun_domain.txt)")
    target.add_argument('-iR', metavar='START-END', dest="target_range", type=str, default='',
                        help='array from int(start) to int(end) (e.g. 192.168.1.1-192.168.2.100)')
    target.add_argument('-iN', metavar='IP/MASK', dest="target_network", type=str, default='',
                        help='generate IP from IP/MASK. (e.g. 192.168.1.0/24)')
    # api
    api = parser.add_argument_group('API')
    api.add_argument('-aZ', '--zoomeye', metavar='DORK', dest="zoomeye_dork", type=str, default='',
                     help='ZoomEye dork (e.g. "zabbix port:8080")') # 钟馗之眼
    api.add_argument('-aS', '--shodan', metavar='DORK', dest="shodan_dork", type=str, default='',
                     help='Shodan dork.') # shodan
    api.add_argument('-aG', '--google', metavar='DORK', dest="google_dork", type=str, default='',
                     help='Google dork (e.g. "inurl:admin.php")') # google搜索 
    api.add_argument('-aF', '--fofa', metavar='DORK', dest="fofa_dork", type=str, default='',
                     help='FoFa dork (e.g. "banner=users && protocol=ftp")') # fofa
    api.add_argument('--limit', metavar='NUM', dest="api_limit", type=int, default=50,
                     help='Maximum searching results (default:50)') # 搜索数目
    api.add_argument('--offset', metavar='OFFSET', dest="api_offset", type=int, default=0,
                     help="Search offset to begin getting results from (default:0)")
    api.add_argument('--search-type', metavar='TYPE', dest="search_type", action="store", default='host',
                     help="[ZoomEye] search type used in ZoomEye API, web or host (default:host)") # 搜索类型
    # proxy
    proxy = parser.add_argument_group('PROXY')
    api.add_argument('--gproxy', metavar='PROXY', dest="google_proxy", action="store", default=None,
                     help="Use proxy (e.g. \"sock5 127.0.0.1 7070\" or \"http 127.0.0.1 1894\"")


    # output
    output = parser.add_argument_group("Output","Use those options to decide output")
    output.add_argument("-o","--output", dest="output_path", type=str, default="",
                        help="output file name. default in ./output/")
    output.add_argument("-oF", "--no-file", dest="no_output", default=False, action="store_false",
                        help="disable file output")

    if len(sys.argv) == 1:
        sys.argv.append("-h")
    args = parser.parse_args()
    return args

