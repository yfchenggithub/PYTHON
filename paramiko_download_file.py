#!/usr/bin/env python

import paramiko
import sys
import os

HOST = '172.171.48.72'
PORT = 22
t = paramiko.Transport((HOST, PORT))
USERNAME='yfcheng'
PASSWORD='yfcheng'
t.connect(username=USERNAME,password=PASSWORD)

sftp = paramiko.SFTPClient.from_transport(t)
remote_path = '/home/yfcheng/1.txt'
local_path = '/tmp/1.txt'
sftp.get(remote_path, local_path)
t.close()

