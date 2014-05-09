import re
import sys

from urllib import request

def error_msg(msg):
	print(msg)
	exit(1)

if len(sys.argv) < 2:
	error_msg("Incorrect number of args")

cmdline_args = " ".join(sys.argv)

url_match = re.search("-url\s+(\w+.\w+)", cmdline_args)
if not url_match:
	error_msg("Url address not specified")
	
URL = "http://%s" % url_match.group(1)

connection = request.urlopen(URL)
html_content = str(connection.read())
connection.close()

img_matches = re.findall('<img src="(.*?)"', html_content)
if not img_matches:
	error_msg("Website %s does not contain any img tags" % URL)

contains_match = re.search("-contains\s+(\w+.*\w*)\s*-*", cmdline_args)
download_match = re.search("-download", cmdline_args)
if not contains_match:
	for img_match in img_matches:
		print(img_match)
	exit(0)

def process_image(img_url, download=None):
	file = request.urlopen(img_url)
	size = file.headers.get("content-length")
	file.close()
	print("number of bytes = %s " % size)

search_pattern = contains_match.group(1)
for img_match in img_matches:
	if search_pattern in img_match:
		process_image(img_match, download_match)
