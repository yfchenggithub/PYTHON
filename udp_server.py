#!/usr/bin/env python

#create udp server
import socket
import sys

HOST = ''
PORT = 5555
#create udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('socket created')
except socket.error:
	print('fail to create socket')
	sys.exit()

#bind ip port
try:
	s.bind((HOST, PORT))
except socket.error:
	print('bind fail')
	sys.exit()
print('socket bind complete')

while 1:
	data, addr = s.recvfrom(1024)
	if not data:break
	s.sendto(data, addr)
	print(data)
s.close()
