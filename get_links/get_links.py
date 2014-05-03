import re
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

min_points = 0
if len(sys.argv) > 1:
	pts = re.search("pts:\s*(\d+)", " ".join(sys.argv))
	min_points = int(pts.group(1)) if pts else 0

driver = webdriver.Firefox()
driver.get("http://www.reddit.com")
driver.maximize_window()

site_table = driver.find_element(By.ID, "siteTable")
entries = site_table.find_elements(By.CSS_SELECTOR, 'div[class*="thing id"]')

links = []
for entry in entries:
	score = entry.find_element(By.CSS_SELECTOR, 'div[class^="score unvoted"]')
	points = int(score.text)
	
	if points < min_points:
		continue
	
	link = entry.find_element(By.CSS_SELECTOR, 'span.domain a')
	if link.text == "i.imgur.com":
		links.append(entry.find_element(By.CSS_SELECTOR, 'p.title a').get_attribute("href"))
	
for link in links:
	body = driver.find_element(By.CSS_SELECTOR, 'body')
	body.send_keys(Keys.CONTROL + 't')
	body.send_keys(link)
	body.send_keys(Keys.ENTER)

	driver.implicitly_wait(2)