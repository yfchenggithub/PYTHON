#!/usr/bin/env python

import socket

HOST='172.171.51.151'
PORT=3129

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(True)
s.settimeout(3)
s.connect((HOST, PORT))
s.sendall(b'hello python')
data = s.recv(1024)
s.close()
print('server', data)
