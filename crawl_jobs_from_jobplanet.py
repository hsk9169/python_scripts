# -*- Encoding:UTF-8 -*-
import sys
import string
import requests
import re
from bs4 import BeautifulSoup as Soup

BASE_URL='https://www.jobplanet.co.kr/companies/by_industry/'

def get_last_page(soup):
    elem = soup.find('a', 'btn_pglast')['href']
    pattern = r'page='
    matchOB = re.search(pattern, elem)
    start = matchOB.start()
    last_page = elem[int(start)+5:]
    print('last page: '+last_page)
    return last_page

def get_industry_type(soup):
    elem = soup.find('div', 'result').find(text=True).strip()[:-5]
    print('industry: '+elem)
    return elem


f = open('./corps_by_industries', 'w', encoding='utf-8')

list_industry_num = []
for i in range(1,11):
    num = i*100
    list_industry_num.append(num)

for industry_num in list_industry_num:
    req = requests.get(BASE_URL + str(industry_num))
    soup = Soup(req.text, 'html.parser')
    last_page = get_last_page(soup)
    industry = get_industry_type(soup)
    f.write('industry: '+industry)
    f.write('\n')
    for page_num in range(1,int(last_page)):
        detail_page = BASE_URL + str(industry_num) + '?page=' + str(page_num)
        print(detail_page)
        detail_req = requests.get(detail_page)
        detail_soup = Soup(detail_req.text, 'html.parser')
        elem = detail_soup.find_all('dt', 'us_titb_l3')
        for el in elem:
            corp_name = el.find('a').find(text=True)
            print(corp_name)
            f.write(corp_name)
            f.write('\n')
f.close()
