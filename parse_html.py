#!/usr/bin/env python

import os
import sys
import re
import getopt

tem = (sys.argv[0].split("/"))
script_name = tem[len(tem) - 1]

def usage():
	print("%s -i infile -o outfile" % script_name)

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
input_file = ""
output_file = ""

for op,value in opts:
	if op == "-i":
		input_file = value
	elif op == "-o":
		output_file = value
	elif op == "-h":
		usage()
		sys.exit()
	else:
		usage()
		sys.exit()

pic_re = "jpg|png|svg|jpeg|gif"
video_re = "swf"
txt_re = "html|css|js"
reobj = re.compile(r'.*?(http://.*?(%s.*?|%s.*?|%s.*?)).*?' % (pic_re, txt_re, video_re), re.S)
result_file = open(output_file, 'w+')

if os.path.exists(input_file):
	_file = open(input_file)
	lines = _file.readlines()
	if not lines:sys.exit()
	_file.close()
	for line in lines:
		for match in reobj.finditer(line):
			result_file.write(match.group(1).strip())
			result_file.write('\n')
	result_file.close()
else:
	print('%s not exist' % input_file)
