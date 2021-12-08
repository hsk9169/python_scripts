# -*- Encoding:UTF-8 -*-
import sys
import string
import random
import nicknames
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import json

URL_REAL = 'http://ec2-3-17-139-14.us-east-2.compute.amazonaws.com:8000/api/users/create'
URL_DEV = 'http://localhost:8000/api/users/create'

env = sys.argv[1]
num_user = sys.argv[2]

length_email = 8
email_list = []
img_keywords = ['여자 아이돌']
imgUrl_list = []
gender_list = ['male', 'female']

if env == 'DEV':
    url = URL_DEV
elif env == 'REAL':
    url = URL_REAL

def crawling_and_request(name):
    driver = webdriver.Chrome(r'/Users/hans/Downloads/chromedriver')
    driver.get('https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl')
    elem = driver.find_element_by_name('q')
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    imgs = driver.find_elements_by_css_selector('.rg_i.Q4LuWd')
    count = 1
    for img in imgs:
        try:
            img.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath(
                    '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img').get_attribute("src")
            if len(imgUrl) < 500:
                email = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_email))
                email = email + '@gmail.com'
                nickname = nicknames.adjective[random.randrange(0,len(nicknames.adjective))] + nicknames.noun[random.randrange(0,len(nicknames.noun))] 
                print(nickname)
                age = random.randrange(20,80)
                gender = gender_list[age % 2]
                data = {'email': email, 'age': age, 'gender': gender, 'nickname': nickname, 'role': 'mentee', 'interests': '개발자', 'img': imgUrl}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=json.dumps(data))
                response.status_code
                response.text
            count += 1
            if count > num_user:
                break
        except:
            pass
    driver.quit()

for keyword in img_keywords:
    crawling_and_request(keyword)


