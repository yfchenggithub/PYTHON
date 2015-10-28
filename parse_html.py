#!/usr/bin/env python

import os
import sys
import re
import getopt
import logging

tem = (sys.argv[0].split("/"))
script_name = tem[len(tem) - 1]
name, ext = os.path.splitext(script_name)

logger = logging.getLogger(name)
logger.setLevel(logging.DEBUG)

log_name = name + ".log"

if os.path.exists(log_name) and os.path.isfile(log_name):
	os.remove(log_name)

fg = logging.FileHandler(log_name)
fg.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(lineno)d: %(message)s")
fg.setFormatter(formatter)

logger.addHandler(fg)

def usage():
	logger.info("%s -i infile" % script_name)
	logger.info("outfile format: infile.out")

opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
input_file = ""
output_file = ""

for op,value in opts:
	if op == "-i":
		input_file = value
	elif op == "-h":
		usage()
		sys.exit()
	else:
		usage()
		sys.exit()
def core_parse():
	logger.info("parse %s begin" %  input_file)
	output_file = input_file + ".out"
	pic_re = "jpg|png|svg|jpeg|gif"
	video_re = "swf"
	txt_re = "html|css|js|htm|shtml"
	reobj = re.compile(r'.*?"(http://(\w+\.)+[^"]*?(%s|%s|%s))".*?' % (pic_re, txt_re, video_re), re.S)

	result_file = open(output_file, 'w+')
	if os.path.exists(input_file):
		_file = open(input_file)
		lines = _file.readlines()
		if not lines:sys.exit()
		for line in lines:
			for match in reobj.finditer(line):
				result_file.write(match.group(1).strip())
				result_file.write('\n')
		_file.close()
		logger.info("parse %s finish" % input_file)
		logger.info("parse result in %s" % output_file)
	else:
		logger.error("%s not exist" % input_file)

	result_file.close()

if __name__ == "__main__":
	core_parse()
	
