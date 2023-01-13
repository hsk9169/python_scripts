# -*- Encoding:UTF-8 -*-
import sys
import string
import time
import os
import requests
import json

env = sys.argv[1]
topic = ''

if env == 'ALERT':
   topic = URL_DEV
elif env == 'WARN':
    topic = URL_REAL

data = dict(placeId=location['placeId'], address=location['address'], details=location['details'], floor=location['floor'], gender=location['gender'], geolocation=json.dumps(location['geolocation']))
headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        count += 1
    else:
        print('POST done')
        break
