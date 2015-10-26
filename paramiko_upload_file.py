#!/usr/bin/env python

import paramiko

HOST = '172.171.48.72'
PORT = 22
t = paramiko.Transport((HOST, PORT))

USERNAME='yfcheng'
PASSWORD='yfcheng'
t.connect(username=USERNAME, password=PASSWORD)

sftp = paramiko.SFTPClient.from_transport(t)
remote_path = '/home/yfcheng/2.txt'
local_path = '/tmp/2.txt'
sftp.put(local_path, remote_path)
t.close()
