from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import requests
import json
import telegram
from threading import Timer

DEPARTURE      = '수서'
ARRIVAL        = '부산'
DATE           = '2022.01.28'
DEPARTURE_TIME = '16시 이후'
NUM_PEOPLE     = '어른(만 13세 이상) 2명'
USER_ID        = '1890491639'
PASSWORD       = 'q0n4l2e5!'

HOME_URL   = 'https://etk.srail.kr/main.do'
CHAT_TOKEN = '5064031519:AAHYD_R51lAD7BNxT3hITfSfslxUbzvkvOQ'
CHAT_ID    = '5000017631'
CHAT_URL   = f'https://api.telegram.org/bot{CHAT_TOKEN}/sendmessage?chat_id={CHAT_ID}&text='

COUNT = 50
COUNT_WAIT = 50

class TicketMacroBot:
    def __init__(self):
        self.driver_options = webdriver.ChromeOptions()
        self.driver_options.add_argument('headless')
        self.driver = webdriver.Chrome(r'/Users/hans/Downloads/chromedriver 2', options=self.driver_options)
        #self.driver = webdriver.Chrome(r'/Users/hans/Downloads/chromedriver 2')
        self.timer_expired = False
        self.loggin = False
        print(DEPARTURE)
        print(ARRIVAL)
        print(DATE)
        print(DEPARTURE_TIME)
        print(NUM_PEOPLE)

    def start_driver(self):
        self.driver = webdriver.Chrome(r'/Users/hans/Downloads/chromedriver 2', options=self.driver_options)

    def close_driver(self):
        self.driver.quit()

    def search_ticket(self):
        # Main Search Page
        self.driver.get(HOME_URL)
        dpt_sel = Select(self.driver.find_element_by_name('dptRsStnCd'))
        dpt_sel.select_by_visible_text(DEPARTURE)
        arv_sel = Select(self.driver.find_element_by_name('arvRsStnCd'))
        arv_sel.select_by_visible_text(ARRIVAL)
        date_sel = self.driver.find_element_by_name('dptDt')
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', date_sel)
        date_sel.clear()
        date_sel.send_keys(DATE)
        dptTm_sel = Select(self.driver.find_element_by_name('dptTm'))
        dptTm_sel.select_by_visible_text(DEPARTURE_TIME)
        tktNum_sel = Select(self.driver.find_element_by_name('psgInfoPerPrnb1'))
        tktNum_sel.select_by_visible_text(NUM_PEOPLE)
        self.driver.find_element_by_link_text("간편조회하기").click()

    def click_reservation(self):
        self.driver.find_element_by_link_text('예약하기').click()
    
    def sign_in(self):
        self.loggin = True
        idInput = self.driver.find_element_by_id('srchDvNm01')
        idInput.send_keys(USER_ID)
        pwdInput = self.driver.find_element_by_id('hmpgPwdCphd01')
        pwdInput.send_keys(PASSWORD)
        self.driver.find_element_by_xpath("//input[@type='submit' and @value='확인']").click()
    
    def send_message(self):
        dptTime = self.driver.find_element_by_xpath("//td[@class='dptTm']")
        message = f'{NUM_PEOPLE} tickets from {DEPARTURE} to {ARRIVAL} at {DATE} {dptTime.text} has been reserved! Please pay for tickets in 10 minutes :) Thank you'
        message_url = CHAT_URL + message
        res = requests.get(message_url)
        return res.status_code 

def timer_expired_func(bot):
   bot.timer_expired = True
   bot.driver.quit()
   bot.loggin = False
   print('===== Timer Expired =====')

if __name__ == '__main__':
    bot = TicketMacroBot()
    
    while True:
        if bot.timer_expired:
            bot.timer_expired = False
            bot.start_driver()
        bot.search_ticket()
        count = 0
        while True:
            if count < COUNT_WAIT:
                try:
                    bot.click_reservation()
                    count = 0
                    print('reservation info input success')
                    break
                except:
                    count += 1
                    pass
            else:
                timer_expired_func(bot)
                break
        while True:
            if not bot.timer_expired:
                if count < COUNT:
                    if not bot.loggin:
                        try:
                            bot.sign_in()
                            count = 0
                            print('sign in success')
                            break
                        except:
                            count += 1
                            pass
                    else:
                        break
                else:
                    timer_expired_func(bot)
                    break
            else:
                break
        #while True:
        #    try:
        #        press_enter_for_special_seat(driver) 
        #        break
        #    except:
        #        pass

        while True:
            if not bot.timer_expired:
                try:
                    res = bot.send_message()
                    break
                except:
                    message = 'reservation failed' 
                    message_url = CHAT_URL + message
                    res = requests.get(message_url)
                    break
            else:
                message = 'reservation failed' 
                message_url = CHAT_URL + message
                res = requests.get(message_url)
                break
