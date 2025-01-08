from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from browser_driver import BrowserDriver

class EdgeDriver(BrowserDriver):
    """Edge 브라우저 드라이버를 관리하는 클래스"""

    def create_options(self):
        return EdgeOptions()

    def start_driver(self, background_mode=False, window_size="1920,1080"):
        options = self.get_options(background_mode=background_mode, window_size=window_size)
        edge_service = EdgeService()
        driver = webdriver.Edge(service=edge_service, options=options)
        print("Edge 브라우저 드라이버 시작됨")
        return driver
