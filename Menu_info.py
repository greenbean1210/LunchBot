import requests
import json
from datetime import date


allergen_dict = {
        '1': '난류',
        '2': '우유',
        '3': '메밀',
        '4': '땅콩',
        '5': '대두',
        '6': '밀',
        '7': '고등어',
        '8': '게',
        '9': '새우',
        '10': '돼지고기',
        '11': '복숭아',
        '12': '토마토',
        '13': '아황산류',
        '14': '호두',
        '15': '닭고기',
        '16': '쇠고기',
        '17': '오징어',
        '18': '조개류'
    }

# API 값 설정 
AUTH_KEY = "5fa6eda3af554790ab2cfe260d464fce"
ATPT_OFCDC_SC_CODE = "J10"
SD_SCHUL_CODE = "7530767"


def get_today_menu(AUTH_KEY, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE):
    # 오늘의 날짜 가져오기
    today = date.today().strftime("%Y%m%d")

    # API 요청을 위한 URL 생성
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={AUTH_KEY}&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}&SD_SCHUL_CODE={SD_SCHUL_CODE}&MLSV_YMD={today}"

    # API 요청 보내기
    response = requests.get(url)
    
    if response.status_code == 200:
        # JSON 데이터 파싱
        data = json.loads(response.text)

        # API 반환값에서 'CODE': 'INFO-200' 부분을 감지
        if 'RESULT' in data and data['RESULT']['CODE'] == 'INFO-200':
            return "API 요청에 오류가 발생했습니다."

        # 메뉴 정보 추출
        menu_string = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]

        # <br/> 태그를 기준으로 문자열을 분리하여 리스트로 저장
        menu_list = menu_string.split('<br/>')

        # 공백 문자 제거
        menu_list_allergiesinfo = [menu.strip() for menu in menu_list if menu.strip()]

        return menu_list_allergiesinfo
    else:
        return "API 요청에 실패했습니다."


def check_menu(menu_raw):
    # 공백 문자 제거 및 알레르기 정보 삭제
    menu_list = [menu.strip().split('(')[0].strip() for menu in menu_raw if menu.strip()]

    return menu_list

def check_allergies(menu_raw):
    allergens_detected = set()

    for menu in menu_raw:
        menu_parts = menu.split(" (")
        # menu_name = menu_parts[0]

        if len(menu_parts) > 1:
            allergens = menu_parts[1].replace(")", "").split(".")
            for allergen in allergens:
                allergen_name = allergen_dict.get(allergen)
                if allergen_name:
                    allergens_detected.add(allergen_name)

    if allergens_detected:
        allergens_list = list(allergens_detected)
        return allergens_list

def get_menu_info():
    # 오늘의 급식 정보 받아오기
    menu_raw = get_today_menu(AUTH_KEY, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE)

    if menu_raw == "API 요청에 오류가 발생했습니다.":
        print("API 요청에 실패했습니다.")
        return ["APIfail"]

    else:
        # today_menu = check_menu(menu_raw)
        today_menu = check_menu(get_today_menu(AUTH_KEY, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE))
        today_allergens = check_allergies(menu_raw)

        return today_menu, today_allergens

print(get_menu_info())


# print(today_menu)
# print(today_allergens)

# get_today_menu(AUTH_KEY, ATPT_OFCDC_SC_CODE, SD_SCHUL_CODE)