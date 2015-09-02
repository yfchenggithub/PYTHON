#!/usr/bin/env python

import socket
import struct
import time


regis_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_addr = ('172.171.51.151', 3130)

register_url = b'url://icp_lap_register'
url_len = len(register_url)
msg_format = '!BBHIIII' + str(url_len) + 's'
msg_len = struct.calcsize(msg_format)
print('msg_len %d' % msg_len)

uc_opcode = 15
uc_version = 4
us_length = msg_len
ui_reqnum = 199
ui_flags = 0
ui_pad = 0

register_ip = '172.171.48.72'
ui_shostid = struct.unpack("!L", socket.inet_aton(register_ip))[0]
register_msg = struct.pack(msg_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid, register_url)

try:
	print('send LAP register msg')
	regis_sock.sendto(register_msg, serv_addr)
finally:
	print('close socket')
	regis_sock.close()


HOST = '172.171.48.72'
PORT = 3129
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('listen to 3129 succ')
client, addr = s.accept()
print('client by', addr)

data = client.recv(1024)
if not data:
	print('no data')
print('LAP ignore GAP cmd, simulate many reply send to GAP')
uc_opcode = 24 #ICP_LOCAL_DELETE

#url must be end with 0; or GAP will parse error, not know what the end is
delete_url = b'www.sina.com.cn\0'
delete_url_len = len(delete_url)
msg_format = '!BBHIIII' + str(delete_url_len) + 's' 
us_length = struct.calcsize(msg_format)
delete_msg = struct.pack(msg_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid,delete_url)
for i in range(3):
	client.sendall(delete_msg)
	print('send delete_msg succ')
client.close()
s.close()
