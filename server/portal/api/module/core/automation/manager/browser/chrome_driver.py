from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browser_driver import BrowserDriver

class ChromeDriver(BrowserDriver):
    """Chrome 브라우저 드라이버를 관리하는 클래스"""

    def create_options(self):
        return ChromeOptions()

    def start_driver(self, background_mode=False, window_size="1920,1080"):
        options = self.get_options(background_mode=background_mode, window_size=window_size)
        chrome_service = ChromeService()
        driver = webdriver.Chrome(service=chrome_service, options=options)
        print("Chrome 브라우저 드라이버 시작됨")
        return driver
