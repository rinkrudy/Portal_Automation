
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
import pandas as pd



class NaverMapSearcher(WebBrowserAutomator):
    def __init__(self, driver, ui_json):
        super().__init__(driver, ui_json)
        super().init_ui_info("Naver", "Map", ui_json)
        
    def locate_measure_circles(self, x_1,y_1, x_2, y_2):
        icon_offset_width = 30 / 2
        icon_offset_height = 40
        action = ActionBuilder(self._driver)
        action.pointer_action.move_to_location(x_1 + icon_offset_width, y_1 + icon_offset_height)
        action.pointer_action.click()
        time.sleep(2)
        action.pointer_action.move_to_location(x_2 + icon_offset_width, y_2 + icon_offset_height)
        action.pointer_action.click()
        action.perform()
        time.sleep(2)

    def extract_city_district(self,address):
        # 주소를 공백 기준으로 나눔
        parts = address.split()
        # 첫 두 부분만 가져옴 (도시와 구)
        city_district = ' '.join(parts[:2])

        return parts[0], parts[1]

    def check_destination_result(self):
        
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        content_area_divs = soup.find_all('div', class_ = 'search_result_content_area')


        columns = ['상호명', '상호주소', '거리']
        df_shop = pd.DataFrame(columns=columns)

        

        # 현재는 1 페이지만 스크래핑
        for content_area in content_area_divs:
            place_title = content_area.find('strong', class_ = "search_result_title").text
            place_address = content_area.find('div', class_= "search_text_box sub_text").find('span', 'search_text').text

            print(place_title + "," + place_address)

            df_shop = pd.concat([df_shop, pd.DataFrame({"상호명" : [place_title], "상호주소" : [place_address], "거리": -2})], ignore_index=True)

        return df_shop
    
    def check_temp_suggest_list(self, start_location, shop_name):
        super().typeinto("출발지", start_location)
        super().sendhotkey("출발지","Enter")
        time.sleep(2)
        super().typeinto("도착지", shop_name[:-1])
        time.sleep(1)
        super().typeinto("도착지", shop_name[-1])
        time.sleep(2)
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        content_area_divs = soup.find_all('div', class_ = 'place_box')

        columns = ['상호명', '상호주소', '거리']
        df_shop = pd.DataFrame(columns=columns)

        for content_area in content_area_divs:
            place_sub = content_area.find('span', class_= 'place_text sub')
            if place_sub is None:
                continue
            place_address = place_sub.text
            place_title = content_area.find('span', class_ = 'place_text').text

            df_shop = pd.concat([df_shop, pd.DataFrame({"상호명" : [place_title], "상호주소" : [place_address], "거리": -2})], ignore_index=True)

        start_location_on_naver = soup.find('input', class_= 'input_search')['value']
        return start_location_on_naver, df_shop
    
    
    def measure_distance(self, start_location, end_location):
        """
        출발지의 주소와 상호명으로 거리를 측정하는 함수
        :param start_location : 출발지의 주소   ex) 서울특별시 동작구 ...
        :param end_location : 도착지의 주소 이름    ex) 서울특별시 동작구 ...
        :return : "출발지" - "도착지" 측정 거리 ex) 1.2km
        """
        try:
            super().open_browser()
            time.sleep(3)
            super().click_element("길찾기")
        except Exception as e:
            super().open_browser()
            time.sleep(7)
            super().click_element("길찾기")

        time.sleep(1)
        super().click_element("다시입력")
        #출발지 입력
        super().typeinto("출발지", start_location)
        super().sendhotkey("출발지","Enter")
        time.sleep(2)
        #도착지 입력
        super().typeinto("도착지", end_location)
        super().sendhotkey("도착지","Enter")
        time.sleep(2)

        super().click_element("네비게이션")
        time.sleep(3)

        try:
            rect_start = self._driver.execute_script("return document.querySelector('div[type=\"start\"]').getBoundingClientRect();")
            rect_end = self._driver.execute_script("return document.querySelector('div[type=\"goal\"]').getBoundingClientRect();")
        except Exception:
            return -1

        super().click_element("다시입력")
        super().click_element("거리측정")

        self.locate_measure_circles(rect_start['x'], rect_start['y'], rect_end['x'], rect_end['y'])
        distance_element = self._driver.find_element(By.CSS_SELECTOR, "div.label_box em.point")
        unit_element = self._driver.find_element(By.CSS_SELECTOR,"div.label_box")

        # 텍스트 추출
        distance = distance_element.text
        unit = unit_element.text.replace(distance, "").strip()
        super().click_element("거리측정")

        distance = float(distance)
        distance = distance/1000 if unit == "m" else distance
        return distance
    


    
    
    
    def measure_distance_on_naver_with_shopname(self, start_location, shop_name, mode_measure=True):
        """
        출발지의 주소와 상호명으로 거리를 측정하는 함수
        :param start_location : 출발지의 주소   ex) 서울특별시 동작구 ...
        :param shop_name : 상호명의 이름    ex) 아오자이
        :return : "네이버 검색결과 상호명", "상호 주소", {{출발지와의 거리(km)}} // 검색결과가 없을 경우 "None", "None", -1
        """

        try:
            super().open_browser()
            time.sleep(3)
            super().click_element("길찾기")
        except Exception as e:
            super().open_browser()
            time.sleep(7)
            super().click_element("길찾기")

        super().click_element("다시입력")



        start_location_on_naver, df_shop_list = self.check_temp_suggest_list(start_location, shop_name)

        if df_shop_list.empty:
            return "None", "None", -1

        city, district = self.extract_city_district(start_location_on_naver)
        """
        if city == "전라북도":
            city = "전북"
        elif city == "전라남도":
            city = "전남"
        elif city == "경기도":
            city = "경기"
        elif city == "충청북도":
            city = "충북"
        elif city == "충청남도":
            city = "충남"
        elif city == "경상남도":
            city = "경남"
        elif city == "경상북도":
            city = "경북"
        elif city == "서울특별시":
            city = "서울"
        """

        print(df_shop_list)
        df_shop_list = df_shop_list[df_shop_list['상호명'].str.contains(shop_name)]
        df_shop_list = df_shop_list[df_shop_list['상호주소'].str.contains(city)]


        if df_shop_list.empty:
            return "None", "None", -1
        

        print(df_shop_list)

        for index, row in df_shop_list.iterrows():
            end_location = row['상호주소']
            distance = self.measure_distance(start_location, end_location)
            df_shop_list.at[index, "거리"] = distance

        min_distance_row = df_shop_list[df_shop_list['거리'] == df_shop_list['거리'].min()].iloc[0]

        return min_distance_row['상호명'], min_distance_row['상호주소'], min_distance_row['거리']







    

