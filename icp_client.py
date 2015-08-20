#!/usr/bin/env python

import struct
import socket
import time

#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('172.171.51.151', 3129)
while True:
	try:
		sock.connect(server_addr)
	except socket.error:
		print('connect fail, try later')
		time.sleep(3)	
	else:
		break

#create icp msg
icp_url = b"url://icp_from_python"
url_len = len(icp_url)
icp_format = '!BBHIIII' + str(url_len) + 's'
icp_len = struct.calcsize(icp_format)
print('icp_len %d' % icp_len)
uc_opcode = 0
uc_version = 4
us_length = icp_len
ui_reqnum = 99
ui_flags = 0
ui_pad = 0
ui_shostid = 0

icp_msg = struct.pack(icp_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid, icp_url)
try:
	print('send icp cmd msg')
	sock.sendall(icp_msg)
	
finally:
	print('close socket')
	sock.close()
