from pymongo import MongoClient
import datetime
import pprint
from bson.objectid import ObjectId

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def crawl_likeuser():

    # 웹드라이버로 페이스북에 접근해서 로그인 후 페이지 정보에 접근하는 부분
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.implicitly_wait(3)

    driver.get('https://www.facebook.com/login/device-based/regular/login/')
    time.sleep(2)

    elem1 = driver.find_element_by_id("email")
    elem1.send_keys("")
    elem2 = driver.find_element_by_id("pass")
    elem2.send_keys("")
    elem3 = driver.find_element_by_id("loginbutton")
    elem3.click()  # 로그인

    # 페이지 일부로 시험작동중 (고민이 많아요)
    # 전체 페이지를 로드하는 부분(위한)
    driver.get('https://www.facebook.com/hanyang.weehan/settings/?tab=people_and_other_pages')

    time.sleep(5)
    print('okay')

    body = driver.find_element_by_tag_name("body")
    time.sleep(2)
    pagedowns = 3000

    while pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        pagedowns -= 1
        print(pagedowns)

    print('done')

    # 로드 된 html을 가져와 필요한 정보를 추출하는 부분
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.find_all('a', class_='_3cb8')
    print(len(temp))

    # 내 페이지를 좋아하는유저 id의 목록을 만드는 부분
    # id(숫자), 닉네임 으로 딕셔너리
    # id: n~~, nick: ~~
    wehan_users=[]
    i = 0
    for a_tag in temp:
        id = a_tag.attrs['href'].lstrip('/')
        name = a_tag.string
        user = {'id': id, 'nick': name}
        wehan_users.append(user)



    # 전체 페이지를 로드하는 부분(한대전)
    driver.get('https://www.facebook.com/Jebohanyang/settings/?tab=people_and_other_pages')

    time.sleep(5)
    print('okay')

    body = driver.find_element_by_tag_name("body")
    time.sleep(2)
    pagedowns = 3000

    while pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        pagedowns -= 1
        print(pagedowns)

    print('done')

    # 로드 된 html을 가져와 필요한 정보를 추출하는 부분
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    temp2 = soup.find_all('a', class_='_3cb8')
    print(len(temp2))

    # 내 페이지를 좋아하는유저 id의 목록을 만드는 부분
    # id(숫자), 닉네임 으로 딕셔너리
    # id: n~~, nick: ~~
    hdj_users = []
    i = 0
    for a_tag in temp2:
        id = a_tag.attrs['href'].lstrip('/')
        name = a_tag.string
        user = {'id': id, 'nick': name}
        hdj_users.append(user)





    # 인원체크
    print()
    print('위한 인원 :', len(temp))
    print(len(wehan_users))

    print()
    print('한대전 인원 :', len(temp2))
    print(len(hdj_users))



    # ((db에 저장하는 부분))

    # db연결
    client = MongoClient('mongodb://localhost:27017/')

    db = client.dodohan
    print(db.list_collection_names())

    # 컬렉션 생성
    wehan_likers = db.wehan_likers
    wehan_likers.insert(wehan_users)

    hdj_likers=db.hdj_likers
    hdj_likers.insert(hdj_users)

    print(db.list_collection_names())

