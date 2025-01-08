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



class GoogleFinder(WebBrowserAutomator):
    def __init__(self, driver, ui_json):
        super().__init__(driver, ui_json)
        super().init_ui_info("Google", "Search", ui_json)

    def find_by_hospital_doctor(self, hospital, doctor):
        try:
            super().open_browser()
            time.sleep(2)
            search_input = super().find_element("검색창")
        except Exception as e:
            super().open_browser()
            time.sleep(7)
            search_input = super().find_element("검색창")
        print(hospital + " "+ doctor)
        search_input.send_keys(hospital + " "+ doctor)
        search_input.submit()
        time.sleep(3)
        
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        search_results = soup.find_all('div', class_="g")

        data_rows = []
        
        columns = ['검색내용', 'URL']
        df_result = pd.DataFrame(columns=columns)
        
        site_names = soup.select('.VuuXrf')
        titles = soup.select('.yuRUbf')
        contents = soup.select('.VwiC3b')
        
        columns = ['검색내용']
        df_result = pd.DataFrame(columns=columns)
        df_result['검색내용'] = ''

        found_contents = []
        urls = []

        min_length = min(len(titles), len(contents))

        for index in list(range(min_length)):
            check_hospital = False
            site_name = site_names[index].text
            title = titles[index].find('h3').text
            summary_content = contents[index].get_text(strip=True)
            url = titles[index].find('a').get('href')

            
            if doctor in hospital:
                check_hospital = True
            elif (hospital in site_name) or (hospital in title) or (hospital in summary_content):
                check_hospital = True
            else:
                split_site_name = site_name.split()[0]
                split_site_title = title.split()[0]
                if (split_site_name in hospital) or (split_site_title in hospital):
                    check_hospital = True
            if check_hospital == True:
                if(doctor in summary_content) or (doctor in title):
                    print("성공")
                    return site_name + " // "+ title + " // " + summary_content, url
                
            else:
                print("실패")
                return "None", "None"


    def find_by_keyword(self, key_word):
        try:
            super().open_browser()
            time.sleep(2)
            search_input = super().find_element("검색창")
        except Exception as e:
            super().open_browser()
            time.sleep(7)
            search_input = super().find_element("검색창")

        search_input.send_keys(key_word)
        search_input.submit()
        time.sleep(3)

        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        search_results = soup.find_all('div', class_="g")


        data_rows = []
        
        columns = ['검색내용', 'URL']
        df_result = pd.DataFrame(columns=columns)
        

        site_names = soup.select('.VuuXrf')
        titles = soup.select('.yuRUbf')
        contents = soup.select('.VwiC3b')

        
        columns = ['검색내용']
        df_result = pd.DataFrame(columns=columns)
        df_result['검색내용'] = ''

        found_contents = []
        urls = []

        min_length = min(len(titles), len(contents))


        for index in list(range(min_length)):
            print(index)
            h3_tag = titles[index].find('h3')
            text = contents[index].get_text(strip=True)
            url = titles[index].find('a').get('href')

            found_contents.append(site_names[index].text + " // "+ h3_tag.text + " // " + text)
            urls.append(url)
            
        df_result = pd.concat([df_result, pd.DataFrame({"검색내용" : found_contents, "URL" : urls})], ignore_index=True)

        return df_result
    
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
        search_result = soup.find('span', class_="LrzXr")
        try:
            place_name = soup.find('div', class_ = 'PZPZlf ssJ7i B5dxMb').text
        except Exception:
            try:
                place_name = soup.find('div', class_ = 'SPZz6b').find('span').text
            except Exception:
                print("구글 상호 title 탐색 실패 : " + palce_keyword)
                return "None", "None"

        if search_result == None:
            print("구글 탐색 실패 : " + palce_keyword)
            return "None", "None"
        else:
            arr_address = search_result.text.split()
            if len(arr_address) == 1:
                return "None", "None"
            print("구글 탐색 : " + palce_keyword + " -> "+ search_result.text)
            return place_name, search_result.text

