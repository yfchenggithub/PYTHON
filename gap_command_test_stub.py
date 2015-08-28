#!/usr/bin/env python

import socket
import struct
import time

#LAP: 监听tcp端口3129; 发送注册到GAP；接收到GAP的SAMPLE命令之后，模拟发送多个响应回去;
#外部触发条件： GAP: 发送SAMPLE命令到LAP 然后等待LAP的响应 进行相应的处理

#送注册到GAP UDP 3130
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

register_ip = '172.171.51.151'
ui_shostid = struct.unpack("!L", socket.inet_aton(register_ip))[0]
register_msg = struct.pack(msg_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid, register_url)

try:
	print('send LAP register msg')
	regis_sock.sendto(register_msg, serv_addr)
finally:
	print('close socket')
	regis_sock.close()


#听tcp端口3129
HOST = '172.171.51.151'
PORT = 3129
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#重复使用处于TIME_WAIT状态的SOCKET， 只是为了测试方便
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('listen to 3129 succ')
client, addr = s.accept()
print('client by', addr)

while True:
	data = client.recv(1024)
	if not data:break
	print('LAP ignore GAP cmd, simulate many reply send to GAP')
	print('data %s' %data)
	#模拟发送多个响应回去
	uc_opcode = 24 #ICP_LOCAL_DELETE
	delete_url = b'www.sina.com.cn'
	delete_url_len = len(delete_url)
	msg_format = '!BBHIIII' + str(delete_url_len) + 's' 
	us_length = struct.calcsize(msg_format)
	delete_msg = struct.pack(msg_format, uc_opcode, uc_version, us_length, ui_reqnum, ui_flags, ui_pad, ui_shostid,delete_url)
	for i in range(5):
		#这里之前client 写成了s；导致一直产生broken pipe错误
		client.sendall(delete_msg)
		print('%d' %i)
	print('send delete_msg succ')
	
s.close()
