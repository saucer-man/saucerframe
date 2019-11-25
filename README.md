# Saucerframe
[![PyPI version](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE) 

saucerframe是一个基于python3的开源批量POC检测框架，默认使用协程异步请求，支持多线程并发，支持多种指定目标方式，可用于批量POC检测，也可根据需要扩展功能。**欢迎star和pr**

**本项目用来交流学习，切勿用来做违法之事**

# 特点

- 支持多线程并发/协程
- 指定目标支持多种方式
    - 指定单个目标
    - 从文本种获取目标
    - 某一网段获取目标 e.g. 192.168.1.0/24
    - 某一ip段获取目标 192.168.1.0-192.168.2.33
    - 支持多种api批量获取目标: [Shodan](https://www.shodan.io/)、[Zoomeye](https://www.zoomeye.org/)、[Fofa](https://fofa.so)、[Censys](https://censys.io)
- 支持全局代理(socks5|socks4|http)

![](https://github.com/saucer-man/saucerframe/blob/master/doc/eg1.png)

# 更新历史
<details>
<summary>点击查看/关闭</summary>

- 2019-11-25
重写进度条。

- 2019-08-10
增加输出等级，增加模块加载方式，支持同时指定多个poc和多种target加载方式。

- 2019-07-25
封装requests模块，新增全局代理选项，默认随机UA，重写censys api模块。

- 2019-07-14
增加进度条；去除并发数的限制；去除google api；优化了一些模块。

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
```shell
git clone https://github.com/saucer-man/saucerframe.git 
cd saucerframe
pip install -r requirement.txt 
```

使用方法：
```shell
python3 saucerframe.py -h
python3 saucerframe.py --show
python3 saucerframe.py -s script-name -iU target-url 
```

具体的参数说明：
```
# 1. 指定poc脚本(必需,支持同时指定多个poc)
-s redis_unauth,mongodb_unauth

# 2. 指定目标(必需)
-iU www.xxx.com  单个目标
-iF target.txt  从文本中加载
-iR 192.168.1.1-192.168.2.100  根据ip地址范围加载
-iN 192.168.1.0/24  根据网段加载
-aZ "redis"  ZoomEye api加载
-aS "redis"  Shodan api加载
-aC "redis"  Censys api加载
-aF "redis"  Fofa api加载

# 3. 其他(可选)
-h  查看帮助信息
-t 300  并发数(默认100)
--proxy socks5://127.0.0.1:1080  使用sock5代理
-o result.txt  指定输出文件
-v 4 指定终端输出详细级别(1-5, 默认为2)
--show  查看所有poc
-eT  并发采用多线程方式
-eG  并发采用协程方式(默认)
```

# POC编写

介绍已移至[wiki](https://github.com/saucer-man/saucerframe/wiki)

# 感谢

框架起初设计过程中借鉴了[POC-T](https://github.com/Xyntax/POC-T)和[sqlmap](https://github.com/sqlmapproject/sqlmap)等优秀开源项目的部分模式和代码，特此说明和感谢。