#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

json_body = {}
json_body['updateId'] = 102
json_body['moduleType'] = 80
json_body['moduleId'] = 83
json_body['updaterAction'] = 1
json_body['subModuleType'] = 0
json_body['subModuleId'] = 0
json_body['pearlVer'] = ''
json_body['currentVersion'] = '2.2.2.0'
json_body['updateVersion'] = '1.3.0.1'
json_body['pkgUrl'] = 'http://192.168.28.111:8090/inst/probe/probe-1.3.0.1-1.x86_64.rpm'
json_body['dependencies'] = ['http://192.168.28.111:8090/inst/probe/probe-1.2.0.2-1.x86_64.rpm']
json_body['patches'] = ['http://192.168.28.111:8090/inst/probe/setup.xml-1.1.0.3-1.2.0.3.patch']
json_body['execCmd'] = 'ls -lh /tmp'

import sys
if len(sys.argv) != 2:
	sys.stderr.write("usage: %s action_num [0:安装;1:升级;2:卸载]\n" % sys.argv[0])
	sys.exit(1)

#0:安装;1:升级;2:卸载
json_body['updateAction'] = int(sys.argv[1])
json_body_data = json.dumps(json_body)
json_body_bytes = json_body_data.encode('utf-8')

class updater_heartbeat_handler(BaseHTTPRequestHandler):
	def __init__(self, *arg, **kwargs):
		BaseHTTPRequestHandler.__init__(self, *arg, **kwargs)
	def do_POST(self):
		self.send_response(200)
		self.send_header('content-type', 'text/html; charset=ISO-8859-1')
		self.send_header('X-Fnic-Pearl-HB-BodyType', 'updateNotify')
		self.end_headers()
		self.wfile.write(json_body_bytes)

from functools import partial
serv = HTTPServer(('',8089), updater_heartbeat_handler)

import threading
d_mon = threading.Thread(target=serv.serve_forever)
d_mon.start()
