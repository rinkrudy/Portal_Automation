from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import time
from bs4 import BeautifulSoup
import json
from selenium.webdriver.chrome.options import Options




class WebBrowserAutomator:
    def __init__(self, driver, ui_json):
        self._driver = driver
        self._url = ""
        self.dict_ui_by = None
        self.site_name = ""
        self.sub_page = ""

    def open_browser(self):        
        self._driver.get(self._url)

    def init_ui_info(self, site_name, sub_site, ui_json):
        self.site_name = site_name
        self.sub_page = sub_site
        self._url = ui_json[site_name][sub_site]['url']
        self.dict_ui_by = ui_json[site_name][sub_site]["ui"]
    
    def check_ui_info(self, ui_name, ui_type):
        if ui_name in self.dict_ui_by.keys() == False:
            raise Exception("not found ui name : " + ui_name)
        
        target_ui_info = self.dict_ui_by[ui_name]
        if ui_type != None and (target_ui_info["ui_type"] != ui_type):
            raise Exception("not type input ui")
        
        ui_selection_type = target_ui_info["type"]
        ui_selection_value = target_ui_info['value']

        by_type = -1
        if ui_selection_type == "xpath":
            by_type = By.XPATH
        elif ui_selection_type == "css_selector":
            by_type = By.CSS_SELECTOR
        elif ui_selection_type == "id":
            by_type = By.ID
        elif ui_selection_type == "name":
            by_type = By.NAME
        
        return by_type, ui_selection_value
        
    
    def typeinto(self, ui_name, text):
        ui_input = self.find_element(ui_name, "input")
        ui_input.send_keys(text)
        time.sleep(3)
    
    def sendhotkey(self, ui_name,key):
        hotkey = 0
        if key == "Enter":
            hotkey = Keys.ENTER
        elif key == "Home":
            hotkey = Keys.HOME
        elif key == "ESC":
            hotkey = Keys.ESCAPE
        ui_input = self.find_element(ui_name, "input")
        ui_input.send_keys(hotkey)
        time.sleep(3)


    def click_element(self, ui_name):
        ui_element = self.find_element(ui_name)
        ui_element.click()
        time.sleep(3)
    
    def get_element_location(self, ui_info):
        location_rect = self._driver.execute_script("return document.querySelector('" + ui_info +"').getBoundingClientRect();")
        return location_rect

    
    def find_element(self, ui_name, ui_type = None):
        by_type, ui_selection_value = self.check_ui_info(ui_name, ui_type)
        element = self._driver.find_element(by_type, ui_selection_value)
        return element


    