# -*- Encoding:UTF-8 -*-
import sys
import json
import string
import requests

# send line-by-line txt file data to mongoDB

URL_REAL = 'http://ec2-18-191-220-124.us-east-2.compute.amazonaws.com:8000/api/autocomplete/'
URL_DEV = 'http://localhost:8000/api/autocomplete/'

env = sys.argv[1]
input_file = sys.argv[2]

if env == 'DEV':
    url = URL_DEV
elif env == 'REAL':
    url = URL_REAL
if input_file == 'jobs_by_industries':
    url += 'job'
    key = 'job'
elif input_file == 'corps_by_industries':
    url += 'corp'
    key = 'corp'

f = open(f'./{input_file}')
lines = f.readlines()
input_list = []
for data in lines:
    input_list.append(data[:-1])

for payload in input_list:
    if key == 'job':
        data = dict(job=payload)
    elif key == 'corp':
        data = dict(corp=payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(data)
    print(response.status_code)

