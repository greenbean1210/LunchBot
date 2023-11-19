import requests
import json
from datetime import date

def get_today_menu(auth_key, edu_code, school_code):
    # 오늘의 날짜를 가져옵니다.
    today = date.today().strftime("%Y%m%d")

    # API 요청을 위한 URL 생성
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={auth_key}&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={edu_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={today}"

    # 인증키 설정
    headers = {
        "Authorization": auth_key
    }

    # API 요청 보내기
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # JSON 데이터 파싱
        data = json.loads(response.text)

        # 메뉴 정보 추출
        menu_string = data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]

        # <br/> 태그를 기준으로 문자열을 분리하여 리스트로 저장
        menu_list = menu_string.split('<br/>')

        # 공백 문자 제거
        menu_list = [menu.strip() for menu in menu_list if menu.strip()]

        return menu_list
    else:
        return "API 요청에 실패했습니다."

# 사용자 입력 받기
auth_key = "5fa6eda3af554790ab2cfe260d464fce"
edu_code = "J10"
school_code = "7530767"

# 오늘의 급식 정보 받아오기
today_menu = get_today_menu(auth_key, edu_code, school_code)

# 메뉴 출력
for menu in today_menu:
    print(menu)
