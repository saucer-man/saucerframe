# Saucerframe
[![PyPI version](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE) 

saucerframe是一个基于python3的开源批量POC检测框架，支持多线程并发，支持多种指定目标方式，可用于`爆破`|`批量POC`。

**本项目用来交流学习，切勿用来做违法之事**

# 特点

- 支持多线程并发/协程
- 指定目标支持多种方式
    - 指定单个目标
    - 从文本种获取目标
    - 某一网段获取目标 e.g. 192.168.1.0/24
    - 某一ip段获取目标 192.168.1.0-192.168.2.33
    - 支持多种api批量获取目标: [Google](https://cse.google.com/cse)、[Shodan](https://www.shodan.io/)、[Zoomeye](https://www.zoomeye.org/)、[Fofa](https://fofa.so)

![](https://github.com/saucer-man/saucerframe/blob/master/doc/eg1.png)
(thinkphp5远程代码执行shodan批量扫描)

# 更新日志
- 2019-04-18

更改默认并发方式为协程，自动根据扫描数量确定异步并发数量，优化了部分代码逻辑

- 2019-02-26

增加协程模式，利用gevent模块实现异步请求。

- 2018-12-15 

将第三方库colorama、IPy、shodan放进thirdlib中直接引用，减少依赖包的安装

- 2018-12-10 

测试框架编写完成

# Usage


```
usage: python3 saucerframe.py -s thinkphp_rce -aS "thinkphp"

optional arguments:
  -h, --help            show this help message and exit

Engine:
  Decide the working way of engine

  -eT                   Multi-Threaded engine (default choice)
  -eG                   Gevent engine (single-threaded with asynchronous)
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
  --limit NUM           Maximum searching results (default:50)
  --offset OFFSET       Search offset to begin getting results from
                        (default:0)
  --search-type TYPE    [ZoomEye] search type used in ZoomEye API, web or host
                        (default:host)
  --gproxy PROXY        Use proxy (e.g. "sock5 127.0.0.1 7070" or "http
                        127.0.0.1 1894"

Output:
  Use those options to decide output

  -o OUTPUT_PATH, --output OUTPUT_PATH
                        output file name. default in ./output/
  -oF, --no-file        disable file output
```

# POC编写

框架与POC的接口调用位于/lib/controller/engine.py，POC接收目标字符串，返回`Retry(2)`|`True(1)`/`False(0)`，当return其他内容时，则直接输出该内容

**注意：POC模块命名必须为`poc`，或者在/lib/core/setting中修改/增加module命名**

示例:

1、编写一个简单POC验证是否存在git信息泄露，这里我们验证目录下是否存在`/.git/config`

```python
import requests
def poc(target_url):
    url = 'target_url'+'/.git/config'
    try:
        r = requests.get(url)
        if r.status_code == 200 and 'repository' in r.text: # 如果在git信息泄露
            return True # 也可以返回1
        else: # 不存在信息泄露
            return Flase #也可以返回0
    except ConnectionError:
        return 2     # 把target_url再次加入任务队列重新验证(本次验证作废)
```

2、编写爆破脚本，指定目标为爆破密码

```python
def poc(target_password):
    url = 'http://xxx.com/login.php?pass=' + target_password
    try:
        r = requests.get(url)
        if 'success' in r.text:
            return True  # 验证成功，屏幕结果输出为123456
            # return url   # 返回其他字符串，屏幕结果输出为"http://xxx.com/login.php?pass=123456"
            else
        return False # 验证失败，无输出
        return 0     # 同上
    except ConnectionError:
        return 2     # 把target_url再次加入任务队列重新验证(本次验证作废)
```

**建议在脚本中增加错误处理，否则发生错误，整个程序则会停止。**

```python
def poc(url)
    try:
    # 这里写脚本
    except:
        return False
```
# 关于POC库

本来不想重复造轮子，不过没找到python3版本的框架，干脆重写了一个python3的框架。但是POC的设计思想是不变的，有时间我将自己写过的一些脚本改成本项目的POC，传到项目中来。

因为一个人的精力有限，如果您在利用本框架中编写了POC，欢迎通过Issues贡献出您的POC或者邮箱联系我(我的邮箱w502325@qq.com)。我会在wiki贴出插件信息和作者。

# 感谢

框架设计过程中借鉴了[POC-T](https://github.com/Xyntax/POC-T)和[sqlmap](https://github.com/sqlmapproject/sqlmap)等优秀开源项目的部分模式和代码，特此说明和感谢。