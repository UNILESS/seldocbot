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
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome(executable_path='C:/Users/sunup/PycharmProjects/seldocbot/chromedriver_win32/chromedriver.exe', options=options)
driver.get('http://freeforms.co.kr')
driver.implicitly_wait(3)

tag_names = driver.find_element_by_id("top-memu-wrap").find_elements_by_tag_name("a")
i = 1
for tag in tag_names:
    print(i,"번", tag.text.split("\n"))
    i += 1

user_input = int(quote_plus(input('원하는 서식 번호를 입력해주세요')))

if user_input == 1:
    url = "/form100/form_1.html"
elif user_input == 2:
    url = "/form104/form_1.html"
elif user_input == 3:
    url = "/form110/form_1.html"
elif user_input == 4:
    url = "/form116/form_1.html"
elif user_input == 5:
    url = "/form120/form_1.html"
elif user_input == 6:
    url = "/form130/form_1.html"
elif user_input == 7:
    url = "/form140/form_1.html"
elif user_input == 8:
    url = "/form200/form_1.html"
elif user_input == 9:
    url = "/form210/form_1.html"
elif user_input == 10:
    url = "/form220/form_1.html"
elif user_input == 11:
    url = "/form230/form_1.html"


url = f'http://freeforms.co.kr{url}'

'''try:  # 정상 처리
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'subject')))
    doc_list = []
    pageNum = int(driver.find_element_by_class_name('_totalCount').text)
    count = 0

    for i in range(1, pageNum):
        doc_data = driver.find_elements_by_class_name('subject')
        download_data = driver.find_elements_by_class_name('list_thumb')

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
        time.sleep(2)'''