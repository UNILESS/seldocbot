from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

# Headless 크롬 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome(chromedriver, options=options)

driver = webdriver.Chrome('C:/Users/sunup/PycharmProjects/chromedriver_win32/chromedriver.exe')

driver.implicitly_wait(3)
driver.get('http://freeforms.co.kr')

user_input = quote_plus(input('원하는 서식 번호를 입력해주세요'))
time.sleep(3)

try:  # 정상 처리
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'list_title')))  # 해당 태그 존재 여부를 확인하기까지 3초 정지
    theater_list = []
    pageNum = int(driver.find_element_by_class_name('_totalCount').text)
    count = 0

    for i in range(1, pageNum):
        theater_data = driver.find_elements_by_class_name('list_title')
        img_data = driver.find_elements_by_class_name('list_thumb')

        for k in theater_data:
            theater_list.append(k.text.split('\n'))

        for j in img_data:  # 이미지 크롤링
            count += 1
            j.screenshot(f'img/{count}.png')

        driver.find_element_by_xpath("//a[@class='btn_page_next _btnNext on']").click()
        time.sleep(2)  # 웹페이지를 불러오기 위해 2초 정지

for i in range(1, pageNum):
        theater_data = driver.find_elements_by_class_name('list_title')

        for k in theater_data:
            theater_list.append(k.text.split('\n'))

        driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[' + str(1 + j * 5) + ']/a/text()').extract() # //*[@id="content"]/div[4]/div[1]/a
        driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[' + str(2 + j * 5) + ']/a/@href').click # # //*[@id="content"]/div[4]/div[2]/a
        time.sleep(2)