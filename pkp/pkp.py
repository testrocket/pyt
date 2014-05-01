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

line_args = " ".join(sys.argv)

station_from = re.search("from:\s*(\w+\s*\w*)", line_args)
if not station_from:
	print("From station not specified")
	exit(1)

station_to = re.search("to:\s*(\w+\s*\w*)", line_args)
if not station_to:
	print("To station not specified")
	exit(1)
	
now = datetime.datetime.now()
time = datetime.time(now.hour, now.minute)
	
station_time = re.search("time:\s*(\d{1,2}):(\d{1,2})", line_args)
if station_time:
	time = datetime.time(int(station_time.group(1)), int(station_time.group(2)))

driver = webdriver.Firefox()

driver.get("http://www.rozklad-pkp.pl/")
driver.maximize_window()
driver.implicitly_wait(7)

input_from = driver.find_element(By.ID, "from")
input_to = driver.find_element(By.ID, "to")
input_time = driver.find_element(By.ID, "time")

input_from.send_keys(station_from.group(1))
input_to.send_keys(station_to.group(1))

input_time.clear()
input_time.send_keys(str(time))

button = driver.find_element(By.NAME, "start")
button.click()
