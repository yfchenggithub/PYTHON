#!/usr/bin/env python

import socket

HOST=''
PORT=5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'hello python')
data = s.recv(1024)
s.close()
print('recv', data)
