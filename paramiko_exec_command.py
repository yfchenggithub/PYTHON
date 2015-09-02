#!/usr/bin/python


import paramiko
import sys
import os
import string

def usage():
	print('usage:  %s netstat -pan | grep -w 80' % sys.argv[0])

#判断是否输入加入命令行
if len(sys.argv) < 2:
	usage()
	sys.exit(1)

#命令弄成字符串形式
input_cmd = ' '.join(sys.argv[1:])

#A high-level representation of a session with an SSH server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#连接服务器 用户名密码
ssh.connect('172.171.48.72', 22, 'yfcheng','yfcheng')

#执行命令
stdin, stdout, stderr = ssh.exec_command(input_cmd)
for line in stdout.readlines():
	print(line)

for line in stderr.readlines():
	print(line)

#关闭连接
ssh.close()
