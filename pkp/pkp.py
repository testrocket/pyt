import sys
import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if len(sys.argv) < 3:
	print("Expected at least 2 arguments - start and stop station")
	exit(1)

line = " ".join(sys.argv)

PATTERN_FROM = re.compile("from:\s*(\w+\s*\w*)")
PATTERN_TO = re.compile("to:\s*(\w+\s*\w*)")
PATTERN_TIME = re.compile("time:\s*(\d{1,2}):(\d{1,2})")

station_from = PATTERN_FROM.findall(line)
if not station_from:
	print("From station not specified")
	exit(1)

station_to = PATTERN_TO.findall(line)
if not station_to:
	print("To station not specified")
	exit(1)
	
now = datetime.datetime.now()
time = datetime.time(now.hour, now.minute)
	
station_time = PATTERN_TIME.findall(line)
if station_time:
	time = datetime.time(int(station_time[0][0]), int(station_time[0][1]))

driver = webdriver.Firefox()

driver.get("http://www.rozklad-pkp.pl/")
driver.maximize_window()
driver.implicitly_wait(7)

input_from = driver.find_element(By.ID, "from")
input_to = driver.find_element(By.ID, "to")
input_time = driver.find_element(By.ID, "time")

input_from.send_keys(station_from)
input_to.send_keys(station_to)

input_time.clear()
input_time.send_keys(str(time))

button = driver.find_element(By.NAME, "start")
button.click()
