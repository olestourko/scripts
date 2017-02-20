#!/usr/bin/env python
from __future__ import print_function
from lxml import html
from lxml.cssselect import CSSSelector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time
import datetime
from datetime import date, timedelta
import json

class GetFaresTask:
    browser = None

    def __del__(self):
        if self.browser:
            self.browser.close()

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
        time.sleep(1) #Allow the dropdowns to appear
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
            #Get the fare times and transfers. An exception will be thrown if the correct fields aren't found (happens when no fares left on this date)
            try:
                fare = {
                        "depart": row.xpath(CSSSelector(".ptStep2departCol").path)[0].text, #.text returns the text before the first element
                        "arrive": row.xpath(CSSSelector(".ptStep2arriveCol").path)[0].text,
                        "duration": row.xpath(CSSSelector(".ptStep2travelTimeCol").path)[0].text,
                        "transfers": row.xpath(CSSSelector(".ptStep2transfersCol").path)[0].text
                }
            except:
                continue

            #Get the fare price. If the price isn't found (sold out/unavailable), it will default to None.
            try:
                fare["web_price"] = row.xpath(CSSSelector(".ptStep2f1 label input").path)[0].tail #.tail is a bit like .text, but it returns everything after the element's closing tag.
            except:
                fare["web_price"] = None

            fares.append(fare)

        return fares

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrapes the Greyhound Canada website for fares across a specified date range.')
    parser.add_argument('--origin', '-o', dest='origin', help='the origin, as it appears in the dropdown on the website', required=True)
    parser.add_argument('--destination', '-d', dest='destination', help='the destination, as it appears in the dropdown on the website', required=True)
    parser.add_argument('--from-date', '-f', dest='from_date', help='the starting date (d/m/Y)', required=False, default=date.today())
    parser.add_argument('--to-date', '-t', dest='to_date', help='the ending date (d/m/Y)', required=False, default=date.today())
    args = parser.parse_args()

    if type(args.from_date) is str:
        args.from_date = datetime.datetime.strptime(args.from_date, "%d/%m/%Y").date() #returns datetime otherwise

    if type(args.to_date) is str:
        args.to_date = datetime.datetime.strptime(args.to_date, "%d/%m/%Y").date()


    delta = args.to_date - args.from_date
    get_fares_task = GetFaresTask()
    schedules = dict()
    for i in range(delta.days + 1):
        date = (args.from_date + timedelta(i)).strftime("%d/%m/%Y")
        fares = get_fares_task.get_fares(origin=args.origin, destination=args.destination, date=date)
        schedules[date] = fares

    json_schedules = json.dumps(schedules, sort_keys=True, indent=4, separators=(',', ':'))
    print(json_schedules)

#TODO: Dynamically find the elements based on context, in case greyhound changes the IDs or title.
