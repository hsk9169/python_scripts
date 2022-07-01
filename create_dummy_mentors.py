# -*- Encoding:UTF-8 -*-
import sys
import string
import random
import nicknames
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import requests
import json
from requests_toolbelt import MultipartEncoder

URL_REAL = 'http://ec2-18-191-220-124.us-east-2.compute.amazonaws.com:8000/api/user'
URL_DEV = 'http://localhost:8000/api/user'

env = sys.argv[1]
num_user = sys.argv[2]

f = open(f'./corps_by_industries')
lines = f.readlines()
input_list = []
corp_list = []
job_list = []
for name in lines:
    input_list.append(name[:-1])
for el in input_list:
    if el not in corp_list:
        corp_list.append(el)
f.close()
f = open(f'./jobs_by_industries')
lines = f.readlines()
input_list = []
for name in lines:
    input_list.append(name[:-1])
for el in input_list:
    if el not in job_list:
        job_list.append(el)
f.close()

num_images = 0
length_email = 8
img_keywords = ['헐리웃 배우']
email_list = []
nickname_list = []
imgUrl_list = []
location_list = []
gender_list = ['male', 'female']
schedule = [{'day':'화', 'startTime':'18:00', 'endTime':'21:00'}, {'day':'금', 'startTime':'17:00', 'endTime':'22:00'}, {'day':'일', 'startTime':'11:00', 'endTime':'14:00'}]

if env == 'DEV':
    url = URL_DEV
elif env == 'REAL':
    url = URL_REAL

def get_random_email_address():
    while(1):
        email = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_email))
        email = email + '@gmail.com'
        if email not in email_list:
            email_list.append(email)
            break
    return email

def get_random_nickname(num):
    while True:
        nickname = nicknames.adjective[random.randrange(0,len(nicknames.adjective))] + nicknames.noun[random.randrange(0,len(nicknames.noun))] + str(num) 
        if nickname not in nickname_list:
            nickname_list.append(nickname)
            break
    return nickname

def get_images_by_keyword(name):
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('headless')
    driver_options.add_argument('--no-sandbox')
    driver_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(r'/Users/hans/Downloads/chromedriver 4', options=driver_options)
    #driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl')
    driver.get('https://www.google.co.kr/imghp?hl=ko')
    #elem = driver.find_element_by_name('q')
    elem = driver.find_element(By.NAME, 'q')
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)
    #imgs = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
    imgs = driver.find_elements(By.CSS_SELECTOR, '.rg_i.Q4LuWd')
    
    count = 1
    for img in imgs:
        if int(count) <= int(num_user):
            try:
                img.click()
                time.sleep(3)
                #imgUrl = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute('src')
                imgUrl = driver.find_element(By.CSS_SELECTOR, '.n3VNCb').get_attribute('src')
                print(imgUrl)
                imgUrl_list.append(imgUrl)
                count += 1
            except:
                pass
        else:
            break
    driver.quit()

def get_locations_by_keyword(keyword):
    page_num = 1
    is_end = False
    while not(is_end):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?' + f'query={keyword}' + f'&page={page_num}'
        response = requests.get(url, headers={'Authorization':'KakaoAK e343c9f82222cc6cc84c721b9e869b3c'}) 
        json_data = json.loads(response.text)
        meta = json_data['meta']
        documents = json_data['documents']
        is_end = meta['is_end']
        for place in documents:
            location = {'place_name':place['place_name'], 'address_name':place['address_name'], 'road_address_name':place['road_address_name'], 'category_group_name':place['category_group_name'], 'content_id':place['id'], 'place_url':place['place_url'], 'phone':place['phone'], 'geolocation':{'x':place['x'], 'y':place['y'], 'distance':''}}
            location_list.append(location)
        page_num += 1



get_locations_by_keyword('서초동 카페')
for keyword in img_keywords:
    get_images_by_keyword(keyword)
num_images = len(imgUrl_list)
num_locations = len(location_list)
num_corps = len(corp_list)
num_jobs = len(job_list)

count = 1
while True:
    if int(count) <= int(num_user):
        age = random.randrange(20,80)
        gender = gender_list[age % 2]
        nickname = get_random_nickname(count)
        email = get_random_email_address()
        fee = random.randrange(10000,50001,5000)
        years = random.randrange(0, 6)
        topics = []
        location = []
        location.append(location_list[count%num_locations])
        location.append(location_list[0])
        for i in range(10):
            if random.choice([True,False]):
                topics.append(i)
        #data = dict(img=json.dumps(imgUrl_list[count%num_images]), email=json.dumps(email), age=json.dumps(str(age)), gender=json.dumps(gender), nickname=json.dumps(nickname), role=json.dumps('mentee'), job=json.dumps(job_list[count%num_jobs]), company=json.dumps(corp_list[count%num_corps]), years=json.dumps(years), topics=json.dumps(topics), authSelect=json.dumps('0'), isAuth=json.dumps('true'), title=json.dumps('안녕하세요 잘 부탁드려요 ㅎㅎ'), introduce=json.dumps('안녕하세요! 무엇이든 물어보세요 :)'), schedules=json.dumps(schedule), cafes=json.dumps(location_list[count%num_locations]), feeSelect=json.dumps('0'), fee=fee)
        ### for simple test
        data = dict(img=json.dumps(imgUrl_list[count%num_images]), phone=json.dumps(email), age=json.dumps(str(age)), gender=json.dumps(gender), nickname=json.dumps(nickname), role=json.dumps('mentor'), job=json.dumps(job_list[count%num_jobs]), company=json.dumps(corp_list[count%num_corps]), years=json.dumps(years), topics=json.dumps(topics), authSelect=json.dumps('0'), isAuth=json.dumps('true'), title=json.dumps('안녕하세요 잘 부탁드려요 ㅎㅎ'), introduce=json.dumps('안녕하세요! 무엇이든 물어보세요 :)'), schedules=json.dumps(schedule), cafes=json.dumps(location), feeSelect=json.dumps('0'), fee=fee)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        count += 1
    else:
        print('POST done')
        break
