# -*- Encoding:UTF-8 -*-
import sys
import string
import random
import time
import os
import requests
import json
from requests_toolbelt import MultipartEncoder

URL_REAL = 'http://ec2-18-191-220-124.us-east-2.compute.amazonaws.com:8000/api/user'
URL_DEV = 'http://localhost:8000/api/point'

env = sys.argv[1]

location_list = []

if env == 'DEV':
    url = URL_DEV
elif env == 'REAL':
    url = URL_REAL

def get_locations_by_keyword(keyword):
    page_num = 1
    idx = 0
    is_end = False
    while not(is_end):
        url = 'https://dapi.kakao.com/v2/local/search/keyword.json?' + f'query={keyword}' + f'&page={page_num}'
        response = requests.get(url, headers={'Authorization':'KakaoAK e343c9f82222cc6cc84c721b9e869b3c'}) 
        json_data = json.loads(response.text)
        meta = json_data['meta']
        documents = json_data['documents']
        is_end = meta['is_end']
        for place in documents:
            #location = {'placeId': idx, 'details':place['place_name'], 'address':place['address_name'], 'floor': idx, 'gender': idx % 3, 'geolocation':{'lat':place['x'], 'lng':place['y']}, 'etc': '화장실 넘어가는 턱이 좀 높아요'}
            location = {'placeId': idx, 'details':place['place_name'], 'address':place['address_name'], 'floor': idx, 'gender': idx % 3, 'geolocation':{'lat':place['x'], 'lng':place['y']}}
            location_list.append(location)
            idx += 1
        page_num += 1

get_locations_by_keyword('서초동 카페')
num_locations = len(location_list)

count = 1
while True:
    if int(count) < int(num_locations):
        location = location_list[count]
        #data = dict(placeId=location['placeId'], address=location['address'], details=location['details'], floor=location['floor'], gender=location['gender'], geolocation=json.dumps(location['geolocation']), etc=location['etc'])
        data = dict(placeId=location['placeId'], address=location['address'], details=location['details'], floor=location['floor'], gender=location['gender'], geolocation=json.dumps(location['geolocation']))
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        count += 1
    else:
        print('POST done')
        break
