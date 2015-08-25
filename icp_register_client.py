#!/usr/bin/env python

#构造icp udp 注册信息到GAP， 以完成LAP的注册


import struct
import socket
import time

#create udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_addr = ('172.171.48.72', 3130)

#create icp register msg
register_url = b"url://icp_lap_register"
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

register_ip = "172.171.51.151"
ui_shostid = struct.unpack("!L", socket.inet_aton(register_ip))[0]
register_msg = struct.pack(msg_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid, register_url)

try:
	print('send LAP register msg')
	sock.sendto(register_msg, serv_addr)
finally:
	print('close socket')
	sock.close()

