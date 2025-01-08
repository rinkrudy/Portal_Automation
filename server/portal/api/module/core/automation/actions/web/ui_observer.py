from ..action import Action
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Ui_Oberver:
    def __init__(self, ui_info):
        pass
    
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
        