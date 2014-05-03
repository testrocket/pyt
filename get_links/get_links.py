import re
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.reddit.com")
driver.maximize_window()

def get_link(domain_name, min_points):
	site_table = driver.find_element(By.ID, "siteTable")
	entries = site_table.find_elements(By.CSS_SELECTOR, 'div[class*="thing id"]')
	for entry in entries:
		score = entry.find_element(By.CSS_SELECTOR, 'div[class^="score unvoted"]')
		points = int(score.text)
		
		if points < min_points:
			continue
		
		link = entry.find_element(By.CSS_SELECTOR, 'span.domain a')
		if domain_name in link.text:
			yield entry.find_element(By.CSS_SELECTOR, 'p.title a').get_attribute("href")

def new_tab(link):
	body = driver.find_element(By.CSS_SELECTOR, 'body')
	body.send_keys(Keys.CONTROL + 't')
	body.send_keys(link)
	body.send_keys(Keys.ENTER)

line_args = " ".join(sys.argv)

points = re.search("pts:\s*(\d+)", line_args)
min_points = int(points.group(1)) if points else 0
	
domain = re.search("domain:\s*(\w+.\w+)", line_args)
domain_name = domain.group(1) if domain else "imgur.com"

for link in get_link(domain_name, min_points):
	new_tab(link)