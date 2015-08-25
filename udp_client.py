#!/usr/bin/env python

import socket
import sys

#create udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print('fail to create socket')
	sys.exit()

HOST = 'localhost'
PORT = 5555

while 1:
	#msg = input('enter to send message:')
	msg = b"hello this is client python"
	try:
		s.sendto(msg, (HOST, PORT))
		reply, addr = s.recvfrom(1024)
		print('server reply', reply)
	except socket.error:
		print('recvfrom from server fail')
		sys.exit()
