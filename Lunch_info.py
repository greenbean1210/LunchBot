import requests
from bs4 import BeautifulSoup

# 급식 정보를 가져오는 코드
# 지금은 웹크롤링을 사용하지만 나이스 api를 사용해 받아올 예정

# 학교 홈페이지 URL
url = 'https://seongji-h.goeyi.kr/seongji-h/main.do'

def get_menu_info(): 
    response = requests.get(url)
    html = response.text

    # HTML 파싱하기
    soup = BeautifulSoup(html, 'html.parser')

    try:
        #원하는 데이터 찾기: "meal_list" 클래스를 가진 dd 태그 찾기
        menu_info = soup.find('dd', {'class': 'meal_list'}).text
        

    except AttributeError:
        menu_info = "오늘의 식단 데이터가 없습니다."

    return menu_info

