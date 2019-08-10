#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
import argparse


def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    """
    parser = argparse.ArgumentParser(usage='python3 saucerframe.py -s thinkphp_rce -aS "thinkphp" --proxy 127.0.0.1:1080 ')
    
    # engine
    engine = parser.add_argument_group("Engine", "Those options decide the working way of engine")
    engine.add_argument('-eT', dest="engine_thread", default=False, action='store_true',
                        help='Multi-Threaded engine')
    engine.add_argument('-eG', dest="engine_gevent", default=False, action='store_true',
                        help='Gevent engine (single-threaded with asynchronous, default choice)')
    engine.add_argument("-t","--thread",  dest="concurrent_num", type=int, default=100,
                        help="num of concurrent, default 100")
    
    # script
    script = parser.add_argument_group("Script", "Those options decide which script to load")
    script.add_argument("-s", "--script",  dest="script_name", type=str, default="",
                        help="load script by name (-s jboss-rce)")
    script.add_argument('--show', dest="show_scripts", default=False, action='store_true',
                      help='show available script names in ./script/ and exit')    
    # target               
    target = parser.add_argument_group("Target","Those options can be used to load targets")
    target.add_argument("-iU", metavar='TARGET', dest="target_single", type=str, default="",
                        help="scan a single target (e.g. www.wooyun.org)")
    target.add_argument("-iF", metavar='FILE', dest="target_file", type=str, default="",
                        help="load targets from targetFile (e.g. wooyun_domain.txt)")
    target.add_argument('-iR', metavar='START-END', dest="target_range", type=str, default='',
                        help='array from int(start) to int(end) (e.g. 192.168.1.1-192.168.2.100)')
    target.add_argument('-iN', metavar='IP/MASK', dest="target_network", type=str, default='',
                        help='generate IP from IP/MASK. (e.g. 192.168.1.0/24)')
    # api
    api = parser.add_argument_group('API', "Those options can be used to load targets with api")
    api.add_argument('-aZ', '--zoomeye', metavar='DORK', dest="zoomeye_dork", type=str, default='',
                     help='ZoomEye dork (e.g. "zabbix port:8080")') 
    api.add_argument('-aS', '--shodan', metavar='DORK', dest="shodan_dork", type=str, default='',
                     help='Shodan dork.') 
    api.add_argument('-aF', '--fofa', metavar='DORK', dest="fofa_dork", type=str, default='',
                     help='FoFa dork (e.g. "banner=users && protocol=ftp")')
    api.add_argument('-aC', '--censys', metavar='DORK', dest="censys_dork", type=str, default='',
                     help='censys dork ')
    api.add_argument('--limit', metavar='NUM', dest="api_limit", type=int, default=100,
                     help='Maximum searching results (default:50)') 
    api.add_argument('--offset', metavar='OFFSET', dest="api_offset", type=int, default=0,
                     help="Search offset to begin getting results from (default:0)")
    api.add_argument('--search-type', metavar='TYPE', dest="search_type", action="store", default='host',
                     help="[ZoomEye] search type used in ZoomEye API, web or host (default:host)") # search type

    # output
    output = parser.add_argument_group("Output","Those options can be used to set output path and filename")
    output.add_argument("-o","--output", dest="output_path", type=str, default="",
                        help="output file name. default in ./output/")
    output.add_argument("-v", "--verbose", dest="logging_level", type=int, default=2,
                        help="logging level, default WARNING,(eg -v 3) to output more")
    
    # proxy
    proxy = parser.add_argument_group("Proxy","Those options can be used to set proxy")
    proxy.add_argument("--proxy", metavar='PROXY', dest="proxy", type=str, default='', help="connect to target with proxy (e.g. 'socks5://127.0.0.1:1080')")

    args = parser.parse_args()
    return args

