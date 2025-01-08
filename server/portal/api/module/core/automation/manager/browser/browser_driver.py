from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from abc import ABC, abstractmethod

class BrowserDriver(ABC):
    """브라우저 드라이버를 관리하는 부모 클래스"""

    def get_options(self, background_mode=False, window_size=None):
        """공통 옵션 설정 메서드"""
        options = self.create_options()
        if background_mode:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            print("Background Mode")
        else:
            options.add_experimental_option("detach", True)
            print("Front Mode")
        
        # SSL 오류 무시 옵션
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")

        # 창 크기 설정
        if window_size:
            options.add_argument(f"--window-size={window_size}")
        
        return options

    @abstractmethod
    def create_options(self):
        """브라우저별 옵션을 생성하는 추상 메서드, 자식 클래스에서 구현"""
        pass

    @abstractmethod
    def start_driver(self, **kwargs):
        """브라우저 드라이버 시작 메서드, 자식 클래스에서 구현"""
        pass
