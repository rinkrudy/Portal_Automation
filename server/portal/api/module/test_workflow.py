from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.chrome.options import Options

import time
from bs4 import BeautifulSoup
import os
import pandas as pd
import json
import re
# custom libs
import sys
sys.path.append("C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/api/module")
from core.module.naver.map_searcher import NaverMapSearcher
from core.module.google.google_finder import GoogleFinder

import math
import requests
sys.path.append("C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/")
from api.models import TaskStatus, HospitalInfo, DoctorInfo, PlaceInfo, Transaction





def haversine(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (km)
    R = 6371.0
    
    # 위도와 경도를 라디안 단위로 변환
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # 위도와 경도의 차이 계산
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine 공식 계산
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 두 지점 사이의 거리 계산 (km)
    distance = R * c
    
    return distance

def get_lat_lon_vworld(address, api_key):
    url = "http://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getCoord",
        "version": "2.0",
        "crs": "epsg:4326",  # WGS84 좌표계
        "address": address,
        "refine": "true",
        "simple": "false",
        "format": "json",
        "type": "road",  # 도로명 주소 또는 'parcel'을 사용할 수 있음
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if result['response']['status'] == 'OK':
            location = result['response']['result']['point']
            lat = location['y']
            lon = location['x']
            print(f"Address : {address}, Coord : {str(lat)}, {str(lon)}")
            return float(lat), float(lon)
        else:
            print(f"Error: {result['response']['status']}")
            return None, None
    else:
        print(f"Error: {response.status_code}")
        return None, None



def get_substring_before_delimiter(input_string):
    pattern = r'[^,(]+'
    match = re.match(pattern, input_string)
    if match:
        return match.group(0)
    else:
        return input_string

def extract_city_district(address):
    # 주소를 공백 기준으로 나눔
    parts = address.split()
    # 첫 두 부분만 가져옴 (도시와 구)
    city_district = ' '.join(parts[:2])
    
    return city_district

def check_array_elements_in_string(input_string1, input_string2):
    # 첫 번째 문자열을 공백을 기준으로 분리하여 배열로 만듭니다.
    array1 = input_string1.split()

    # 배열의 모든 원소가 두 번째 문자열에 포함되어 있는지 확인합니다.
    for element in array1:
        if element not in input_string2:
            return False

    return True

def read_excel(file_path, sheet_name, start_row_index = 0):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=start_row_index)
    return df

def save_excel(file_path, sheet_name, dt_src):
    excel_writer = pd.ExcelWriter(file_path, engine='openpyxl')
    dt_src.to_excel(excel_writer, sheet_name = sheet_name, index= False)
    excel_writer._save()


def init_dataframe(df):
    if '검증결과' not in df.columns:
        df['검증결과'] = ''
    if '주소(소속)' not in df.columns:
        df['주소(소속)'] = ''
    if '상호명(검색)' not in df.columns:
        df['상호명(검색)'] = ''
    if '주소(상호)' not in df.columns:
        df['주소(상호)'] = ''
    if ("좌표_소속" in df.columns) == False:
        df['좌표_소속'] = ""
    if ("좌표_상호" in df.columns) == False:
        df['좌표_상호'] = ""

    if '거리' not in df.columns:
        df['거리'] = -2
    if ("검색포탈" in df.columns) == False:
        df['검색포탈'] = ""

    if ("의료인검색결과" in df.columns) == False:
        df['의료인검색결과'] = ""


    if ("URL" in df.columns)== False:
        df["URL"] = ""

    
    return df

def create_transactions(df, task_id):
    for index, row in df.iterrows():
        Transaction.objects.create(
            tx_key = task_id,
            hospital_name = row["소속"],
            hospital_number = row["요양기관기호"],
            doctor_name = row["성명"],
            place_name = row["장소"]
                                    )

    
# "CREATED",
# "MAPPING_MEDICAL_CARE",
# "FIND_DOCTOR",
# "FIND_PLACE",
# "MEASURE_DISTANCE"
def update_task_step(task_id, step):
    task = TaskStatus.objects.get(task_id = task_id)
    task.step = step
    task.save()

def update_value(task_id, key, value):
    task = TaskStatus.objects.get(task_id = task_id)
    task[key] = value
    task.save()


def Test_WorkFlow(df_input, task_id, background_mode):
    create_transactions(df_input, task_id)
    task = TaskStatus.objects.get(task_id = task_id)
    print("Start Workflow")
    print(df_input)
    df_origin = init_dataframe(df_input)
    base_dir = "C:/Users/User/Documents/Code/Python/RobotFramework/test_docs"
    api_key = "0D4E3693-FFC1-39EF-8C70-1F4328D54E29"  
    excel_요양기관번호_path = os.path.join(base_dir, "리스트_요양기관기호.xlsx")
    df_basis_key = read_excel(excel_요양기관번호_path, "요양기관 현황", 3)

    task.step = "MAPPING_MEDICAL_CARE"
    task.save()
    
    for index, row in df_origin.iterrows():
        address = ""
        medical_result = ""
        try:
            hospital_info = HospitalInfo.objects.get(hospital_number=row["요양기관기호"])
            address = hospital_info.hospital_address
            df_origin.at[index, "주소(소속)"] = address
            medical_result = "확인"
        except HospitalInfo.DoesNotExist:
            try:
                address = get_substring_before_delimiter((df_basis_key[df_basis_key['요양기관 기호'] == row["요양기관기호"]]).iloc[0]["도로명주소"])
                df_origin.at[index, "주소(소속)"] = address
                HospitalInfo.objects.create(
                    hospital_number = row["요양기관기호"],
                    hospital_name = row["소속"],
                    hospital_address = address
                )
                medical_result = "확인"
            except Exception as e:
                address = "None"
                print(f'요양기관기호 탐색 실패 : {row["요양기관기호"]}')
                medical_result = "확인실패"

        tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
        tx.hospital_address = address
        tx.medical_exist = medical_result
        tx.save()

        

    failed_mapping_count = len(df_origin[pd.isna(df_origin["주소(소속)"])])




    # 요양기관번호 매칭 후 테스트
    naver_map = None
    google_finder = None
    bing_seacher = None



    dict_place_check = {}

    options = Options()
    print(background_mode)
    if background_mode:
        options.add_argument("--headless")  # 백그라운드(헤드리스) 모드로 실행
        options.add_argument("--disable-gpu")  # GPU 가속을 비활성화 (헤드리스 모드에서 권장)
        options.add_argument("--no-sandbox")   # 일부 환경에서는 필요할 수 있음
        options.add_argument("--disable-dev-shm-usage")  # 리소스 사용 최소화
        print("Background Mode")
    else:
        options.add_experimental_option("detach", True)  # 브라우저가 자동으로 닫히지 않도록 함
        print("Front Mode")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-erros")
    

    # # 웹 드라이버 초기화 
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    print("리소스 로드 시작")


    task.step = "FIND_DOCTOR"
    task.save()
    work_count_doctor = 0
    failed_count_doctor = 0
    with open("C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/api/module/resource/ui_info.json", 'r', encoding="UTF8") as txt:
        json_data = json.load(txt)
        print(json_data)
        google_finder = GoogleFinder(driver, json_data)

    for index, row in df_origin.iterrows():
        work_count_doctor += 1
        try:
            google_finder.open_browser()
        except Exception as e:
            google_finder.open_browser()
            time.sleep(7)


        name = row['성명']
        hospital = row['소속']
        
        try:
            doctor_info = DoctorInfo.objects.get(hospital_key = str(row["요양기관기호"]), doctor_name = name)
            df_origin.at[index, '검색포탈'] = "DB"
            df_origin.at[index, '의료인검색결과'] = "DB 데이터 존재"
            tx = Transaction.objects.get(tx_key = task_id, hospital_number = row["요양기관기호"], doctor_name = row["성명"])
            tx.doctor_exist = "확인"
            tx.save()
        except DoctorInfo.DoesNotExist:
            try:
                find_result, url = google_finder.find_by_hospital_doctor(hospital, name)
                df_origin.at[index, '검색포탈'] = "Google"
                if find_result == "None":
                    df_origin.at[index, '의료인검색결과'] = "확인실패"
                    failed_count_doctor += 1
                    tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
                    tx.doctor_exist = "확인 불가"
                    tx.save()
                else:
                    df_origin.at[index, '의료인검색결과'] = find_result
                    df_origin.at[index, 'URL'] = url
                    tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
                    tx.doctor_exist = "확인"
                    tx.save()
                    DoctorInfo.objects.create(hospital_key = str(row["요양기관기호"]), doctor_name = name)

            except Exception as e:
                df_origin.at[index, '검색포탈'] = "Google"
                df_origin.at[index, '의료인검색결과'] = "Error"
                df_origin.at[index, 'URL'] = "None"
                failed_count_doctor += 1
                tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
                tx.doctor_exist = "확인 불가"
                tx.save()
            
        task.work_count_doctor = work_count_doctor
        task.failed_count_doctor = failed_count_doctor
        task.save()

        
        # count += 1

        # if count > 30:
        #     print("Browser reboot")
        #     count = 0
        #     driver.quit()
        #     time.sleep(3)
        #     driver = webdriver.Chrome(options=options)
        #     driver.maximize_window()

        #     naver_map = None
        #     with open("./resource/ui_info.json", 'r', encoding="UTF8") as txt:
        #         json_data = json.load(txt)
        #         google_finder = GoogleFinder(driver, json_data)

    

    print(df_origin)



    naver_map = NaverMapSearcher(driver, json_data)
    google_finder = GoogleFinder(driver, json_data)



        # bing_seacher = BingSearcher(driver, json_data)
    #



    # df_origin = read_excel(test_excel_path, "Result")    


    

    work_count_place = 0
    failed_count_place = 0
    # 상호명(검색) / 상호주소(검색)
    task.step = "FIND_PLACE"
    task.save()
    for index, row in df_origin.iterrows():
        work_count_place += 1

        # Mapping에 실패한 데이터 넘김
        if (row['주소(소속)'] == None) or (pd.isna(row["주소(소속)"]) == True):
            df_origin[index, "거리"] = -2
            failed_count_place += 1
            task.work_count_place= work_count_place
            task.failed_count_place = failed_count_place
            task.save()
            tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
            tx.searched_address = "확인 불가"
            tx.place_exist = "확인 불가"
            tx.save()
            continue

        if (row['주소(상호)'] != '') and (pd.isna(row["주소(상호)"]) == False):
            print("skip")
            print(row['주소(상호)'])
            failed_count_place += 1
            task.work_count_place= work_count_place
            task.failed_count_place = failed_count_place
            task.save()
            tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
            tx.searched_address = "확인 불가"
            tx.place_exist = "확인 불가"
            tx.save()
            continue

        # 소속 의료기관과 지출처 장소가 같다면?
        place_name = row["장소"]

        if row['소속'] == place_name:
            df_origin.at[index, "거리"] = 0
            task.work_count_place= work_count_place
            task.failed_count_place = failed_count_place
            task.save()
            tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
            tx.searched_address = "요양기관내"
            tx.place_exist = "확인"
            tx.save()
            continue
        
        place_name = row['장소']
        place_key = str(row['요양기관기호']) + "_" + row['장소']
        place_address = ""

        try:
            place_info = PlaceInfo.objects.get(place_key = place_key)
            place_name = place_info.place_name
            place_address = place_info.place_address

        except PlaceInfo.DoesNotExist:
            searched_place_name, searched_address = google_finder.find_place(place_name)

            if len(searched_address.split(" ")) < 3:
                place_name = "확인 필요"
                place_address = searched_address
                failed_count_place += 1
            else:
                place_name = searched_place_name
                place_address = searched_address.split(" KR")[0]
                PlaceInfo.objects.create(place_key = place_key, place_name = place_name, place_address = place_address)


            if pd.isna(searched_place_name) == True:
                place_name = "확인 필요"
                place_address = "확인 필요"
                failed_count_place += 1
            
        
        df_origin.at[index, "상호명(검색)"] = place_name
        df_origin.at[index, "주소(상호)"] = place_address

        tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
        tx.searched_address = place_address

        if (place_name == "확인 필요"):
            tx.place_exist = "확인 불가"
        else:
            tx.place_exist = "확인"
        tx.save()
        task.work_count_place= work_count_place
        task.failed_count_place = failed_count_place
        task.save()
    # print(df_input)



    work_count_measure = 0
    failed_count_measure = 0
    
    # # vWorld를 통한 좌표 생성
    task.step = "MEASURE_DISTANCE"
    task.save()
    for index, row in df_origin.iterrows():
        work_count_measure += 1
        is_measurable = False
        if row['거리'] != -2:
            failed_count_measure += 1
            continue

        # Mapping에 실패한 데이터 넘김
        if (row['주소(소속)'] == None) or (pd.isna(row["주소(소속)"]) == True):
            df_origin.at[index, "거리"] = -2
            failed_count_measure += 1
            continue
        
        if (row['주소(상호)'] == 'None'):
            failed_count_measure += 1
            continue

        is_measurable = True
        if is_measurable == False:
            failed_count_measure += 1
            task.work_count_measure = work_count_measure
            task.failed_count_measure = failed_count_measure
            task.save()
        else:
            if row['소속'] == row['장소']:
                df_origin.at[index, "거리"] = 0
                tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
                tx.distance = 0
                tx.save()
                task.work_count_measure = work_count_measure
                task.failed_count_measure = failed_count_measure
                task.save()
                continue 

        
        location_start = row["주소(소속)"]
        location_end = row['주소(상호)']

        try:
            hospital_info = HospitalInfo.objects.get(hospital_number = str(row['요양기관기호']))
        except HospitalInfo.DoesNotExist:
            df_origin.at[index, "거리"] = -2
            failed_count_measure += 1
            task.work_count_measure = work_count_measure
            task.failed_count_measure = failed_count_measure
            task.save()
            continue

        try:
            place_key = str(row['요양기관기호']) + "_" + row['장소']
            place_info = PlaceInfo.objects.get(place_key = place_key)
        except PlaceInfo.DoesNotExist:
            df_origin.at[index, "거리"] = -2
            failed_count_measure += 1
            task.work_count_measure = work_count_measure
            task.failed_count_measure = failed_count_measure
            task.save()
            continue

        lat1 = -1
        lon1 = -1
        if (hospital_info.coord_lat == -1):
            lat1, lon1 = get_lat_lon_vworld(location_start, api_key)
            if lat1 is not None:
                df_origin.at[index, "좌표_소속"] = str(lat1) + "," + str(lon1) 
                hospital_info.coord_lat = lat1
                hospital_info.coord_lon = lon1
                hospital_info.save()
            else:
                df_origin.at[index, "거리"] = -2
                failed_count_measure += 1
                task.work_count_measure = work_count_measure
                task.failed_count_measure = failed_count_measure
                task.save()
        
        lat1 = hospital_info.coord_lat
        lon1 = hospital_info.coord_lon


        if (place_info.coord_lat == -1):
            lat2, lon2 = get_lat_lon_vworld(location_end, api_key)
            if lat2 is not None:
                df_origin.at[index, "좌표_상호"] = str(lat2) + "," + str(lon2)
                place_info.coord_lat = lat2
                place_info.coord_lon = lon2
                place_info.save()
            else:
                df_origin.at[index, "거리"] = -2
                failed_count_measure += 1
                task.work_count_measure = work_count_measure
                task.failed_count_measure = failed_count_measure
                task.save()
    
        lat2 = place_info.coord_lat
        lon2 = place_info.coord_lon

        distance = 0

        if (lat2 is not None) and (lat1 is not None):
            distance = haversine(lat1, lon1, lat2, lon2)
            df_origin.at[index, "거리"] = distance
            print(distance)

        tx = Transaction.objects.get(tx_key = task_id, hospital_number = str(row["요양기관기호"]), doctor_name = row["성명"])
        tx.distance = distance
        tx.save()
        
        task.work_count_measure = work_count_measure
        task.failed_count_measure = failed_count_measure
        task.save()

    task.step = "FINISHED"
    task.save()


    #     if count > 2:
    #         print("Browser reboot")
    #         count = 0
    #         driver.quit()
    #         time.sleep(3)
    #         driver = webdriver.Chrome(options=options)
    #         driver.maximize_window()

    #         naver_map = None
    #         with open("./resource/ui_info.json", 'r', encoding="UTF8") as txt:
    #             json_data = json.load(txt)
    #             naver_map = NaverMapSearcher(driver, json_data)
    #             google_finder = GoogleFinder(driver, json_data)
    #             # bing_seacher = BingSearcher(driver, json_data)
            
    #         save_excel(test_excel_path, "Result", df_origin)    
        

        
    #     count += 1
    #     place_check_key = location_start + "|" + place_name
    #     if place_check_key in dict_place_check.keys():
    #         df_origin.at[index, "상호명(검색)"] = shopname_on_naver
    #         df_origin.at[index, "주소(상호)"] = address_on_naver
    #         df_origin.at[index, "거리"] = distance
    #         continue
    #     else:
    #         dict_place_check[place_check_key] = ["", "", -2]

    #     shopname_on_naver, address_on_naver, distance = naver_map.measure_distance_on_naver_with_shopname(location_start, place_name)
    #     df_origin.at[index, "상호명(검색)"] = shopname_on_naver
    #     df_origin.at[index, "주소(상호)"] = address_on_naver
    #     df_origin.at[index, "거리"] = distance
        
    #     dict_place_check[place_check_key] = [shopname_on_naver, address_on_naver, distance]

#save_excel(test_excel_path, "Result", df_origin)


    driver.quit()
    count = 0
    # 네이버를 통해 거리 조회


    # options = Options()
    # options.add_experimental_option("detach", True)  # 브라우저가 자동으로 닫히지 않도록 함
    # print("Front Mode")

    # options.add_argument("--ignore-ssl-errors=yes")
    # options.add_argument("--ignore-certificate-erros")
    

    # # # 웹 드라이버 초기화 
    # driver = webdriver.Chrome(options=options)
    # driver.maximize_window()
    
    # print("리소스 로드 시작")

    # for index, row in df_origin.iterrows():
    #     # # Mapping에 실패한 데이터 넘김
    #     # if (row['주소(소속)'] == None) or (pd.isna(row["주소(소속)"]) == True):
    #     #     df_origin.at[index, "거리"] = -2
    #     #     continue
    #     # if (row['주소(상호)'] != '') and (pd.isna(row["주소(상호)"]) == False):
    #     #     print("skip")
    #     #     print(row['주소(상호)'])
    #     #     continue
      
    #     # # 소속 의료기관과 지출처 장소가 같다면?
    #     # place_name = row["장소"]
    #     # if row['소속'] == place_name:
    #     #     print("소속 == 장소")
    #     #     df_origin.at[index, "거리"] = 0
    #     #     continue
    #     # location_start = row["주소(소속)"]
      
    #     if (row["거리"] >= 0):
    #         continue

    #     if count > 4:
    #         print("Browser reboot")
    #         count = 0
    #         driver.quit()
    #         time.sleep(3)
    #         driver = webdriver.Chrome(options=options)
    #         driver.maximize_window()
    #         naver_map = None
    #         with open("C:/Users/User/Documents/Code/Projects/RPA/Portal/server/portal/api/module/resource/ui_info.json", 'r', encoding="UTF8") as txt:
    #             json_data = json.load(txt)
    #             naver_map = NaverMapSearcher(driver, json_data)
    #             # google_finder = GoogleFinder(driver, json_data)
    #             # bing_seacher = BingSearcher(driver, json_data)


    #     place_check_key = location_start + "|" + place_name
    #     if place_check_key in dict_place_check.keys():
    #         df_origin.at[index, "상호명(검색)"] = shopname_on_naver
    #         df_origin.at[index, "주소(상호)"] = address_on_naver
    #         df_origin.at[index, "거리"] = distance
    #         continue
    #     else:
    #         dict_place_check[place_check_key] = ["", "", -2]
    #     shopname_on_naver, address_on_naver, distance = naver_map.measure_distance_on_naver_with_shopname(location_start, place_name)
    #     df_origin.at[index, "상호명(검색)"] = shopname_on_naver
    #     df_origin.at[index, "주소(상호)"] = address_on_naver
    #     df_origin.at[index, "거리"] = distance
    #     df_origin.at[index, "검색포탈"] = "Naver"

    #     dict_place_check[place_check_key] = [shopname_on_naver, address_on_naver, distance]

    
    for index, row in df_origin.iterrows():
        failed_list = []
        result_text = ""
        if row["의료인검색결과"] == "확인실패":
            failed_list.append("인적사항 확인불가")
        
        if row["거리"] > 10:
            failed_list.append("거리점검 필요")
        
        if pd.isna(row["주소(소속)"]) == True:
            failed_list.append("요양기관 주소 확인 불가")
        
        if row["주소(상호)"] == "None":
            failed_list.append("상호 주소 확인 불가")

        

        
        if len(failed_list) == 0:
            result_text = "검증성공"
        else:
            result_text = "/".join(failed_list)

        df_origin.at[index, "검증결과"] = result_text




    return df_origin


#save_excel(test_excel_path, "Result", df_origin)

