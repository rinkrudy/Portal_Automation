from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.chrome.options import Options
from enum import Enum

class Brower_Type(Enum):
    NoneBrowser = 0
    Chrome = 1
    Edge = 2
    FireFox = 3


class WebDriver:
    def __init__(self, browser_type : Brower_Type, background_mode = True, maximize = True):
        self.__driver = None
        self.__background_mode = background_mode
        self.__browser_type = browser_type
        self.__maximize = maximize
        self.__create_driver(background_mode=background_mode, browser_type= browser_type)

        if self.__driver == None:
            raise ValueError("Driver initialize is failed")

        if self.__maximize == True:
            self.__driver.maximize_window()

    
    @property
    def driver(self):
        return self.__driver    
        
    # @driver.setter
    # def driver(self, value):
    #     if value == None:
    #         raise ValueError("instance of driver is null")
    #     self.__driver = value


    def __create_driver(self, background_mode=True):
        options = Options()
        if background_mode:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        else:
            options.add_experimental_option("detach", True)
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")

        # 각 호출마다 독립적인 Chrome 인스턴스 생성
        if self.__browser_type == Brower_Type.Chrome:
            self.__driver = webdriver.Chrome(options=options)
        elif self.__browser_type == Brower_Type.Edge:
            self.__driver = webdriver.Edge(options=options)
        elif self.__browser_type == Brower_Type.FireFox:
            self.__driver = webdriver.Firefox(options=options)
        else:
            raise ValueError("Not Suport Browser Type")

        self.__driver.maximize_window()
