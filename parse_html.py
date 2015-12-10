#!/usr/bin/env python
"""
author: yfcheng
date:2015-12-2
email:18912964525@163.com
description: just for pre-cache feature; administrator select the website and tell us to pre-cache them only
"""
import os
import sys
import re
import getopt
import logging
import requests
import shutil
import glob

def init_log(_filename, _format, _level):
	logging.basicConfig(filename=_filename,
			filemode='w',
			format=_format,
			level=_level)
	logging.info("log name: %s", _filename)

def log_extension_name():
	return '.log'

def log_name(_script_name):
	tem = (sys.argv[0].split("/"))
	script_name = tem[len(tem) - 1]
	name, ext = os.path.splitext(_script_name)
	name += log_extension_name() 
	return name

def log_format():
	return "%(asctime)s %(name)s [%(levelname)s] %(lineno)d: %(message)s"

def log_level():
	return logging.DEBUG

def print_usage():
	logging.info("script_name -i infile -o outfile")

def exit_program():
	"""
		exit program; exit status code 1; later add exit status code as input argument
	"""
	sys.exit(1) 

def whitelist_extension_name():
	"""
	whitelist extension name; according this name to judge this file type 
	"""
	return '.wle' 
 
def homepage_extension_name():
	"""
	according to extension name to know the file type
	"""
	return '.hpe'

def backup_extension_name():
	"""
	backup file extension name
	"""
	return '.bak'

def parse_opt(option):
	"""
	parse option; current option -h -i -o support only; option default sys.argv[1:]
	"""
	try:
		opts, args = getopt.getopt(option, "hi:o:")
	except getopt.GetoptError as err:
		print(str(err))
		print_usage()
		exit_program()

	input_file = None
	output_file = None
	for op, value in opts:
		if op == "-i":
			input_file = value
			continue
		if op == "-o":
			output_file = value
			continue
		if op == "-h":
			print_usage()
			exit_program()

	if not input_file:
		logging.error("not input file; exit")
		exit_program()

	if not output_file:
		logging.warning("user not specify output file; take default output file")
		output_file = input_file + whitelist_extension_name() 

	logging.info("input_file: %s output_file: %s",input_file, output_file)

def create_file(new_file):
	os.mknod(new_file)

def write_data_to_file(data, file):
	"""
	copy data to file
	"""
	if not data:
		logging.error('no content, exit')
		exit_program()

	default_file = file
	if not default_file:
		logging.warning('no specify file to save; default file')
		default_file = "default_file"
		logging.info('default_file %s', default_file)
	
	if os.path.exists(default_file):
		os.remove(default_file)
	create_file(default_file)

	fd = os.open(default_file, os.O_RDWR)
	byte_written = os.write(fd, data)
	os.close(fd)
	logging.info('write %d bytes data to file %s succ', byte_written, file)
	return default_file 
			
def bak_file(file):
	"""
	backup file
	"""
	bak_file_name = file + backup_extension_name() 
	shutil.copyfile(file, bak_file_name)	
	logging.info('copy file %s to %s succ', file, bak_file_name)
	return bak_file_name

def get_whitelist_txt_uri():
	return 'http://172.171.51.154:8888/txt/website.txt'
 	
def fetch_and_save_whitelist_txt(whitelist_url, file):
	"""
	fetch the whitelist from the web admin, save the data to file
	"""
	_tmp_file = None
	logging.info('fetch_whitelist_txt begin')
	r = requests.get(whitelist_url)
	if 200 != r.status_code:
		logging.critical('fetch whitelist fail; exit')	
		exit_program()
	logging.info('fetch whitelist succ')
	logging.info('whitelist content:\n%s', r.text)
	_tmp_file = write_data_to_file(r.content, file) 
	logging.info('save whitelist txt to %s succ', _tmp_file)
	bak_file(_tmp_file)
	return _tmp_file

def video_site_set_support():
	"""
	support video web set 
	"""
	return ['iqiyi', 'youku', 'tudou', 'hunantv', 'letv', 'ku6']

def business_site_set_support():
	"""
	support business web set
	"""
	return ['jd', 'tmall', 'yhd', 'amazon', 'dangdang', 'taobao']

def webpage_site_set_support():
	"""
	browse webpage site set to support
	"""
	return ['baidu', 'sina', 'hao123', 'csdn', 'zhihu', '36kr', 'lagou', 'hupu']
	
def get_support_web_set():
	"""
	support website set; later make it configurable
	"""
	_video_set = video_site_set_support()
	_business_set = business_site_set_support()
	_webpage_set = webpage_site_set_support()
	return (_video_set + _business_set + _webpage_set)	

def webpage_directory_name():
	return 'webpage'

def create_webpage_directory():
	_old_dir = os.getcwd()
	_webpage_dir = webpage_directory_name()
	os.mkdir(_webpage_dir)
	os.chdir(_webpage_dir)
	_dir_set = webpage_site_set_support()
	for _dir in _dir_set:
		os.mkdir(_dir)
	os.chdir(_old_dir)

def business_directory_name():
	return 'business'

def create_business_directory():
	_old_dir = os.getcwd()
	_business_dir = business_directory_name()
	os.mkdir(_business_dir)
	os.chdir(_business_dir)
	_dir_set = business_site_set_support()
	for _dir in _dir_set:
		os.mkdir(_dir)
	os.chdir(_old_dir)

def video_directory_name():
	return 'video'

def create_video_directory():
	_video_dir_dirs = video_site_set_support()
	_old_dir = os.getcwd()
	_video_dir = video_directory_name()
	os.mkdir(_video_dir)
	os.chdir(_video_dir)
	_dir_set = video_site_set_support()
	for _dir in _dir_set:
		os.mkdir(_dir)
	os.chdir(_old_dir)	

def whitelist_txt_directory_name():
	return 'txt'

def create_whitelist_txt_directory():
	_txt_dir = whitelist_txt_directory_name()
	os.mkdir(_txt_dir)
	
def create_all_directory():
	create_video_directory()
	create_business_directory()
	create_webpage_directory()
	create_whitelist_txt_directory()
	logging.info('create_all_directory')

def delete_directory(dir):
	shutil.rmtree(dir, True)

def delete_video_directory():
	_video_dir = video_directory_name()
	delete_directory(_video_dir)

def delete_webpage_directory():
	_webpage_dir = webpage_directory_name()
	delete_directory(_webpage_dir)

def delete_business_directory():
	_business_dir = business_directory_name()
	delete_directory(_business_dir)

def delete_whitelist_txt_directory():
	_txt_dir = whitelist_txt_directory_name()
	delete_directory(_txt_dir)

def delete_all_directory():
	delete_video_directory()
	delete_business_directory()
	delete_webpage_directory()
	delete_whitelist_txt_directory()
	logging.info('delete_all_directory')

def file_name_separator():
	return '.'

def file_need_classify(_file):
	"""
	only file start with [baidu youku sina] need classify
	"""
	_separator = file_name_separator() 
	_dir = _file.split(_separator)[0]
	_need_classify = False
	_cur_dirs = get_support_web_set()
	if _dir in _cur_dirs:
		_need_classify = True
	else:
		_need_classify = False
	return _need_classify
	
def file_classify_category(_file):
	"""
	according the file give the right category;[business, webpage, video]
	"""
	_separator = file_name_separator()
	_key = _file.split(_separator)[0]
	if _key in webpage_site_set_support():
		return webpage_directory_name()

	if _key in video_site_set_support():
		return video_directory_name()

	if _key in business_site_set_support():
		return business_directory_name()

def path_separator():
	return '/'

def file_classify_dir(_file):
	"""
	according to the file name to get the classify directory
	"""
	_classify_dir = os.getcwd()
	_separator = file_name_separator()
	_dir = file_classify_category(_file)
	_classify_dir += path_separator()
	_classify_dir += _dir
	_classify_dir += path_separator()
	_classify_dir += _file.split(_separator)[0]	
	return _classify_dir	

def classify_whitelist():
	"""
	in the current directory classify the whitelist like baidu.homepage.out to the diretory baidu
	"""
	_files = os.listdir('.')
	for _file in _files:
		if os.path.isdir(_file):
			continue
		if file_need_classify(_file):
			_dir = file_classify_dir(_file)
			shutil.move(_file, _dir)		
			logging.info('file %s move to dir %s', _file, _dir)

def website_support(website):
	"""
	should the website [baidu youku] support
	"""
	_support = False
	support_web_key_set = get_support_web_set() 
	for web_key in support_web_key_set:
		if web_key in website:
			_support = True
			break
	return _support
				
def home_page_name(website):
	"""
	file name for website home page
	"""
	home_page = None
	web_key_set = get_support_web_set()
	for web_key in web_key_set:
		if web_key in website:
			home_page = web_key + homepage_extension_name() 
	return home_page	

def detele_repeat_url(_file):
	"""
	url may be repeated; url should be unique; file must be parsed 
	"""
	_repeat_file_name = _file + '.rep'
	os.rename(_file, _repeat_file_name)
	old_lines = open(_repeat_file_name).readlines()
	new_line = set()
	count = 0
	_new_file_name = _file
	_new_file = open(_file, 'w')
	for line in old_lines:
		if line in new_line:
			count += 1
			continue
		new_line.add(line)
		_new_file.write(line)
	_new_file.close()
	os.remove(_repeat_file_name)
	logging.info('file %s have %d lines repeat, already delete', _file, count)

def fetch_and_save_home_page(whitelist_txt):
	"""
	fetch and save the website home page according to the whitelist txt
	"""
	reobj = born_resource_pattern_obj() 
	if os.path.exists(whitelist_txt):
		_file = open(whitelist_txt)
		lines = _file.readlines()
		if not lines: exit_program()
		for line in lines:
			line = line.strip('\n')
			logging.info('ready to fetch_web_page %s', line)
			r = requests.get(line)
			website = line	
			if not website_support(website):
				logging.warning('website %s not support; next', website)
				continue

			if 200 != r.status_code:
				logging.warning('get %s fail, status code %d', line, r.status_code)
				continue
			else:
				logging.info('get %s succ, statuc code %d', line, r.status_code)
				_result_file = home_page_name(website)
				write_data_to_file(r.content, _result_file)
				_parse_file = core_parse(_result_file, reobj)
				detele_repeat_url(_parse_file)
	else:
		logging.error('not found file %s, exit program', whitelist_txt)
		exit_program()

def picture_pattern():
	"""
	current picture pattern should match
	"""
	return "jpg|png|svg|jpeg|gif"

def video_pattern():
	"""
	current video pattern should match
	"""
	return "swf|avi|rm|rmvb|mpg|mpeg|wmv|asf"

def text_pattern():
	"""
	current text pattern should match
	"""
	return "html|css|js|htm|shtml"
	 		
def pattern_str():
	"""
	re compile pattern str
	"""
	pic_re = picture_pattern() 
	video_re = video_pattern()
	txt_re = text_pattern() 
	str = r'.*?"(http://(\w+\.)+[^"]*?(%s|%s|%s))".*?' % (pic_re, txt_re, video_re)
	return str

def pattern_flag():
	""" 
	re compile flags
	"""
	return re.S

def born_resource_pattern_obj():
	_str = pattern_str()
	_flag = pattern_flag()
	_reobj = re.compile(_str, _flag)
	return _reobj

def core_parse(html_file, reobj):
	"""
	parse the html_file and find all the resource url and save them
	"""
	logging.info("parse %s begin" %  html_file)
	output_file = html_file + whitelist_extension_name() 

	result_file = open(output_file, 'w+')
	if os.path.exists(html_file):
		data = open(html_file).read()
		for match in reobj.findall(data):
			result_file.write(match[0])
			result_file.write('\n')
		logging.info("parse %s finish" % html_file)
		logging.info("parse result in %s" % output_file)
	else:
		logging.error("%s not exist" % html_file)
	result_file.close()
	return output_file

def whitelist_name():
	return 'whitelist.txt'

def whitelist_put_dir():
	"""
	the directory put the whitelist txt; every txt size not larger than 16kB
	"""
	_txt_dir = whitelist_txt_directory_name()
	_cwd_dir = os.getcwd()
	_dir = os.path.join(_cwd_dir, _txt_dir)
	return _dir

def split_size():
	"""
	make every whitelist file size not bigger than 16KB
	"""
	return 1024 * 16

def split_fix_lines():
	"""
	split big files to small files have 150 lines at most
	"""
	return 150

def do_split(_file_2_split):
	"""
	split file 
	"""
	_result_files = []
	_dir_name = os.path.dirname(_file_2_split)
	_file_name = os.path.basename(_file_2_split)
	_file = open(_file_2_split, 'r')
	_lines = _file.readlines()
	_line_num = len(_lines)
	logging.info('file %s have lines %d', _file_2_split, _line_num)
	_left_num = _line_num
	_part_index = 0
	_fix_lines = split_fix_lines()
	_begin_line = 0
	_end_line = split_fix_lines()
	while 1:
		if _left_num < _fix_lines: 
			filename = _dir_name + '/' +  _file_name + ('%04d' % _part_index)
			fileobj = open(filename, 'w')
			_part_data = _lines[_begin_line:]
			for _line in _part_data:
				fileobj.write(_line)
			fileobj.close()
			_result_files.append(filename)
			break
		_part_data = _lines[_begin_line:_end_line]
		filename = _dir_name + '/' +  _file_name + ('%04d' % _part_index)
		fileobj = open(filename, 'w')
		for _line in _part_data:
			fileobj.write(_line)
		fileobj.close()
		_part_index += 1
		_begin_line += _fix_lines
		_end_line += _fix_lines
		_left_num -= _fix_lines 
		_result_files.append(filename)
	_file.close()		
	return _result_files

def spilt_file():
	"""
	whitelist txt must be smaller than 16kB; larger file should be split
	"""
	_spilt_size = split_size()
	_search_pattern = os.getcwd() + '/*/*/*wle'
	_put_dir = whitelist_put_dir()
	for _file in glob.glob(_search_pattern):
		_file_size = os.path.getsize(_file)
		if _file_size < _spilt_size:
			shutil.copy(_file, _put_dir)
			logging.info('file %s NOT need split; directly move to %s', _file, _put_dir)
		else:
			logging.info('file %s size %d larger than 16KB, need split', _file, _file_size)
			_files_after_split = do_split(_file)
			for _item in _files_after_split:
				if os.path.getsize(_item) >= _spilt_size:
					logging.error('_file %s larger than 16KB after split', _item)
				logging.info('file %s need move to  %s', _item, _put_dir)
				shutil.copy(_item, _put_dir)
				

if __name__ == "__main__":
	_log_name = log_name(sys.argv[0])
	_log_format = log_format()
	_log_level = log_level()
	init_log(_log_name, _log_format, _log_level)
	whitelist_txt_uri = get_whitelist_txt_uri()
	save_file = fetch_and_save_whitelist_txt(whitelist_txt_uri, whitelist_name())
	fetch_and_save_home_page(save_file)
	delete_all_directory()
	create_all_directory()
	classify_whitelist()
	spilt_file()

