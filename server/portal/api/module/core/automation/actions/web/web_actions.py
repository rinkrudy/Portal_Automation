from ..action import Action
from abc import ABC, abstractmethod
import sys
from selenium.webdriver.common.by import By

sys.path.append("../../")
from resources import WebDriver


class Ui_Action(Action):
    def __init__(self, driver, ui_observer, ui_id):
        if ui_observer is None:
            raise ValueError("Ui Observer is not initialized")
        
        self.__ui_observer.check_ui_info() = ui_observer
        
        super().__init__(driver)
        self.__
        pass

    
    def perform(self):
        
        
        

class Mouse_Click(Ui_Action):
    def __init__(self, driver, ui_observer):
        super().__init__(driver, ui_observer)
        if driver is None:
            raise ValueError("Driver's instance is null")
        self.__driver = driver
        
    @classmethod
    @abstractmethod
    def perform(self, **kwargs):
        pass



class Mouse_Click(Ui_Action):
    def __init__(self, driver):
        super().__init__(driver)
    
    def perform(self, **kwargs):
        selector = kwargs["selecor"]
        selctor_type = kwargs["type"]
        
        
        # xpath, css_selector
        element = self.__driver.find_element("")
        
        
        
        


