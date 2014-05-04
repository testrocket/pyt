import re
import sys

from urllib import request

if len(sys.argv) < 2:
	print("Incorrect number of args")
	exit(1)

cmdline_args = " ".join(sys.argv)

url_match = re.search("-url\s+(\w+.\w+)", cmdline_args)
if not url_match:
	print("Url address not specified")
	exit(1)
	
url = "http://%s" % url_match.group(1)

connection = request.urlopen(url)
html_content = str(connection.read())
connection.close()

img_matches = re.findall('<img src="(.*?)"', html_content)
if not img_matches:
	print("Website %s does not contain any img tags" % url)
	exit(1)

contains_match = re.search("-contains\s+(\w+.*\w*) -*", cmdline_args)
download_match = re.search("-download", cmdline_args)
if not contains_match:
	for img_match in img_matches:
		print(img_match)
	exit(0)

def process(img_url, download=None):
	print("number of bytes = %s " %len(request.urlopen(img_url).read()))

contains_pattern = contains_match.group(1)
print("sarch for contains pattern = %s" % contains_pattern)
for img_match in img_matches:
	if contains_pattern in img_match:
		process(img_match, download_match)
