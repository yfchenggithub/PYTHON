#!/usr/bin/env python

#主要是作为白名单的http服务器的客户端  监听端口为8080


import requests
_url = 'http://172.171.51.151:8080'
_headers = {'Want-Type':'whiteList', 'Want-Arg':'baidu/0'}
r = requests.get(_url, headers=_headers)


