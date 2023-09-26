import requests
from bs4 import BeautifulSoup

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
        # menu_info = "배추김치(9.), 영양닭죽(, 오라떼(13.), 에그드랍샌드위치"

    except AttributeError:
        menu_info = "오늘의 식단 데이터가 없습니다."

    return menu_info

#print(get_menu_info())
