# Saucerframe

saucerframe是一个基于python3的开源渗透测试框架，支持多线程并发，支持多种指定目标方式，可用于`爆破`|`批量POC`。

框架设计过程中借鉴了[POC-T](https://github.com/Xyntax/POC-T)和[sqlmap](https://github.com/sqlmapproject/sqlmap)等优秀开源项目的部分模式和代码，特此说明和感谢。

# 优点
- 可扩展性好，根据漏洞编写POC即可批量扫描|爆破
- 支持多线程并发
- 指定目标支持多种方式
    - 指定单个目标
    - 从文本种获取目标
    - 某一网段获取目标 e.g. 192.168.1.0/24
    - 某一ip段获取目标 192.168.1.0-192.168.2.33
    - 支持多种api批量获取目标: [Google](https://cse.google.com/cse)、[Shodan](https://www.shodan.io/)、[Zoomeye](https://www.zoomeye.org/)、[Fofa](https://fofa.so)

# Usage
```
查看帮助信息:
    -h, --help            show this help message and exit

指定线程:(可选，默认10)
    Decide the threads of engine

    -t THREAD_NUM, --thread THREAD_NUM
                            num of threads, 10 by default

加载POC脚本(必选)
    Choice script you want to use

    -s/--script SCRIPT_NAME 
                        load script by name (-s jboss-rce)
    --show                show available script names in ./script/ and exit

指定目标(必选)
    At least one of these optionshas to be provided to define the target(s)

    -iU TARGET            scan a single target (e.g. www.wooyun.org)
    -iF FILE              load targets from targetFile (e.g. wooyun_domain.txt)
    -iR START-END         array from int(start) to int(end) (e.g.
                        192.168.1.1-192.168.2.100)
    -iN IP/MASK           generate IP from IP/MASK. (e.g. 192.168.1.0/24)

    -API:
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

文件输出:(可选)
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

本框架的模式基于[POC-T](https://github.com/Xyntax/POC-T)，本来不想重复造轮子，不过[POC-T](https://github.com/Xyntax/POC-T)只支持python2，干脆重写了一个python3的框架。但是POC的设计思想是不变的，有精力我会将已有的POC改成python3版本，传到项目中来。

因为一个人的精力有限，如果你在利用本框架中编写了POC，欢迎通过Issues提交。我会在下面贴出插件信息和作者。
