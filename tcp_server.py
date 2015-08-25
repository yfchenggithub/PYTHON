#!/usr/bin/env python
import socket

HOST = ''
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

conn, addr = s.accept()
print('connect by', addr)

while True:
	data = conn.recv(1024)
	if not data:break
	conn.sendall(data)
conn.close()

