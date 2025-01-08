from browser.chrome_driver import ChromeDriver
from browser.edge_driver import EdgeDriver

class DriverManager:
    _instance = None  # 싱글톤 인스턴스

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.drivers = []  # 모든 드라이버 인스턴스를 관리하는 리스트
        return cls._instance

    def start_chrome_driver(self, background_mode=False, window_size="1920,1080"):
        """Chrome 드라이버 인스턴스 생성 및 시작"""
        chrome_driver_manager = ChromeDriver()
        driver = chrome_driver_manager.start_driver(background_mode=background_mode, window_size=window_size)
        self.drivers.append(driver)
        return driver

    def start_edge_driver(self, background_mode=False, window_size="1920,1080"):
        """Edge 드라이버 인스턴스 생성 및 시작"""
        edge_driver_manager = EdgeDriver()
        driver = edge_driver_manager.start_driver(background_mode=background_mode, window_size=window_size)
        self.drivers.append(driver)
        return driver

    def quit_all_drivers(self):
        """모든 드라이버 종료"""
        for driver in self.drivers:
            try:
                driver.quit()
                print("드라이버 종료됨")
            except Exception as e:
                print(f"드라이버 종료 중 오류 발생: {e}")
        self.drivers.clear()  # 리스트 초기화
        print("모든 드라이버 종료 완료")
