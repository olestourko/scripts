from __future__ import print_function
from lxml import html
from lxml import etree
from lxml.cssselect import CSSSelector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date, timedelta

class GetFaresTask:
    browser = None

    def __get_browser(self):
        if not self.browser:
            self.browser = webdriver.Chrome()

        return self.browser

    def get_fares(self, origin, destination, date=None, browser=None):
        browser = self.__get_browser()
        browser.get("https://www.greyhound.ca/")

        #fill out form fields
        origin_input = browser.find_element_by_id("ctl00_body_search_listOrigin_Input")
        destination_input = browser.find_element_by_id("ctl00_body_search_listDestination_Input")

        if date:
            date_input = browser.find_element_by_id("ctl00_body_search_dateDepart_dateInput")
            date_input.clear()
            date_input.send_keys(date)
        
        origin_input.clear()
        origin_input.send_keys(origin)
        destination_input.clear()
        destination_input.send_keys(destination)
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

        fares = list()
        for row in tree.xpath(CSSSelector("table .innerRow").path):
            fare = {
                    "depart": row.xpath(CSSSelector(".ptStep2departCol").path)[0].text, #.text returns the text before the first element
                    "arrive": row.xpath(CSSSelector(".ptStep2arriveCol").path)[0].text,
                    "duration": row.xpath(CSSSelector(".ptStep2travelTimeCol").path)[0].text,
                    "transfers": row.xpath(CSSSelector(".ptStep2transfersCol").path)[0].text
            }

            try:
                fare["web_price"] = row.xpath(CSSSelector(".ptStep2f1 label input").path)[0].tail
            except:
                fare["web_price"] = None

            fares.append(fare)

        return fares

if __name__ == "__main__":
    start_date = date(2017, 02, 18)
    end_date = date(2017, 02, 18)
    delta = end_date - start_date

    get_fares_task = GetFaresTask()

    for i in range(delta.days + 1):
        date = (start_date + timedelta(i)).strftime("%d/%m/%Y")
        fares = get_fares_task.get_fares(origin="London, ON", destination="Toronto, ON", date=date)
        print(fares)

#TODO: Output the results tree as a .csv or something similair
#TODO: Dynamically find the elements based on context, in case greyhound changes the IDs or title.
