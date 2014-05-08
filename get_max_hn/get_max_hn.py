import re

from urllib import request
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com/"

req = request.Request(URL, headers={'User-Agent': 'Dummy browser'})
con = request.urlopen(req)
html_str = str(con.read())
con.close()

soup = BeautifulSoup(html_str)
spans = soup.find_all('span', id=re.compile('^score_\d+'))

max_points = 0
max_span = None
for span in spans:
	scores = re.findall("(\d+)\s+points", span.string)
	
	points = int(scores[0]) if scores else 0
	if points > max_points:
		max_points = points
		max_span = span

# get previous TR element
dom_tr = max_span.parent.parent.previous_sibling

# get anchor with 'href' value
dom_a = dom_tr.contents[2].contents[0]

print("max number of points is: %s" % max_points)
print("URL: %s" % dom_a['href'])
