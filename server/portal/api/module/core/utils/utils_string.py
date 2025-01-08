import re

class Utils_String:
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