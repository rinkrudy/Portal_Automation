
import sys
sys.path.append("../../")
from ..webbrower_automator import WebBrowserAutomator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import time
from bs4 import BeautifulSoup
import json


class BingSearcher(WebBrowserAutomator):
    def __init__(self, driver, ui_json):
        super().__init__(driver, ui_json)
        super().init_ui_info("Bing", "Search", ui_json)
        
    def find_place(self, palce_keyword):
        try:
            super().open_browser()
            time.sleep(2)
            search_input = super().find_element("검색창")
        except Exception as e:
            super().open_browser()
            time.sleep(7)
            search_input = super().find_element("검색창")
        search_input.send_keys(palce_keyword)
        search_input.submit()
        time.sleep(5)

        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        search_result = soup.find('span', class_="bm_details_overlay")

        if search_result == None:
            print("Bing 탐색 실패 : " + palce_keyword)
            return None
        else:
            a_tag = search_result.find('a')
            print("Bing 탐색 : " + palce_keyword + " -> "+ a_tag.text)
            return a_tag.text



