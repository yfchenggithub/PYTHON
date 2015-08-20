#!/usr/bin/env python

import socket
import struct
import sys 

host = '172.171.51.151'
port = 3129
backlog = 5
s = None

icp_url = "url://icp_from_python"
url_len = len(icp_url)
icp_format = '!BBHIIII' + str(url_len) + 's'

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(backlog)
except socket.error:
	if s:
		s.close()
	print('could not open socket')
	sys.exit(1)

while True:
	client, addr = s.accept()
	data = client.recv(1024)
	icp_msg = struct.unpack(icp_format, data)
	for member in icp_msg:
		print(member)
	client.close()
