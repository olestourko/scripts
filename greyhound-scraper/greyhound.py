from __future__ import print_function
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
browser.get("https://www.greyhound.ca/")

#fill out form fields
origin_input = browser.find_element_by_id("ctl00_body_search_listOrigin_Input")
destination_input = browser.find_element_by_id("ctl00_body_search_listDestination_Input")

origin_input.send_keys("London, ON")
destination_input.send_keys("Toronto, ON")
time.sleep(0.5) #Allow the dropdowns to appear
origin_input.send_keys(Keys.ENTER)
destination_input.send_keys(Keys.ENTER)

#submit the form
browser.find_element_by_id("ticketsSearchSchedules").click()

#wait until the results are displayed 
wait = WebDriverWait(browser, 10)
wait.until(EC.title_is("Greyhound.ca | Step 2"))

results_element = browser.find_element_by_id("tableDepart") 
results_html = results_element.get_attribute("innerHTML")
tree = html.fromstring(results_html)

#TODO: Output the results tree as a .csv or something similair
#TODO: Loop through a range of dates
#TODO: Dynamically find the elements based on context, in case greyhound changes the IDs or title.
