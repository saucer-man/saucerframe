# Saucerframe
[![PyPI version](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE) 

saucerframe是一个基于python3的开源批量POC检测框架，默认使用协程异步请求，支持多线程并发，支持多种指定目标方式，可用于批量POC检测，也可根据需要扩展功能。欢迎star和fork。

**本项目用来交流学习，切勿用来做违法之事**

# 特点

- 支持多线程并发/协程
- 指定目标支持多种方式
    - 指定单个目标
    - 从文本种获取目标
    - 某一网段获取目标 e.g. 192.168.1.0/24
    - 某一ip段获取目标 192.168.1.0-192.168.2.33
    - 支持多种api批量获取目标: [Google](https://cse.google.com/cse)、[Shodan](https://www.shodan.io/)、[Zoomeye](https://www.zoomeye.org/)、[Fofa](https://fofa.so)、[Censys](https://censys.io)

![](https://github.com/saucer-man/saucerframe/blob/master/doc/eg1.png)
(利用Zoomeye批量扫描thinkphp5远程代码执行漏洞主机)

<details>
<summary># 更新日志</summary>


- 2019-05-09
增加logging模块，支持输出等级；增加censys api调用；IPY替换为内置库ipaddress、imp更新为importlib模块；规范大部分函数、变量命名；修改了程序逻辑。

- 2019-05-08
增加plugin目录，逐步添加plugin，方便poc调用。目前已添加随机user-agent

- 2019-04-18
更改默认并发方式为协程，自动根据扫描数量确定异步请求数量，优化了部分代码逻辑，速度提升

- 2019-02-26
增加协程模式，利用gevent模块实现异步请求。

- 2018-12-15 
将第三方库colorama、IPy放进thirdlib中直接引用，减少依赖包的安装。

- 2018-12-10 
测试框架编写完成

</details>


# 使用

安装方法：
```
git clone https://github.com/saucer-man/saucerframe.git 
cd saucerframe
pip install -r requirement.txt 
```

使用方法：
```
python3 saucerframe.py -s script-name -iU target-url 
```

具体的参数说明：
```
usage: python3 saucerframe.py -s thinkphp_rce -aS "thinkphp"

optional arguments:
  -h, --help            show this help message and exit

Engine:
  Decide the working way of engine

  -eT                   Multi-Threaded engine
  -eG                   Gevent engine (single-threaded with asynchronous,
                        default choice)
  -t THREAD_NUM, --thread THREAD_NUM
                        num of threads, default 30

Script:
  Choice script you want to use

  -s SCRIPT_NAME, --script SCRIPT_NAME
                        load script by name (-s jboss-rce)
  --show                show available script names in ./script/ and exit

Target:
  At least one of these optionshas to be provided to define the target(s)

  -iU TARGET            scan a single target (e.g. www.wooyun.org)
  -iF FILE              load targets from targetFile (e.g. wooyun_domain.txt)
  -iR START-END         array from int(start) to int(end) (e.g.
                        192.168.1.1-192.168.2.100)
  -iN IP/MASK           generate IP from IP/MASK. (e.g. 192.168.1.0/24)

API:
  -aZ DORK, --zoomeye DORK
                        ZoomEye dork (e.g. "zabbix port:8080")
  -aS DORK, --shodan DORK
                        Shodan dork.
  -aG DORK, --google DORK
                        Google dork (e.g. "inurl:admin.php")
  -aF DORK, --fofa DORK
                        FoFa dork (e.g. "banner=users && protocol=ftp")
  -aC DORK, --censys DORK
                        censys dork
  --limit NUM           Maximum searching results (default:50)
  --offset OFFSET       Search offset to begin getting results from
                        (default:0)
  --search-type TYPE    [ZoomEye] search type used in ZoomEye API, web or host
                        (default:host)

PROXY:
  --gproxy PROXY        Use proxy (e.g. "sock5 127.0.0.1 7070" or "http
                        127.0.0.1 1894"

Output:
  Use those options to decide output

  -o OUTPUT_PATH, --output OUTPUT_PATH
                        output file name. default in ./output/
  -v LOGGING_LEVEL      logging level, default INFO,(eg -v 1) to output more
```

# POC编写

介绍已移至[wiki](https://github.com/saucer-man/saucerframe/wiki)

# 感谢

框架设计过程中借鉴了[POC-T](https://github.com/Xyntax/POC-T)和[sqlmap](https://github.com/sqlmapproject/sqlmap)等优秀开源项目的部分模式和代码，特此说明和感谢。

