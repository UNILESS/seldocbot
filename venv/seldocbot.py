from urllib.parse import quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# 크롬 옵션
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

options.add_experimental_option("prefs", {
    "download.default_directory":
        r"C:/Users/sunup/Desktop/docdown",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(executable_path='C:/Users/sunup/PycharmProjects/seldocbot/chromedriver_win32/chromedriver.exe', options=options)
driver.get('http://freeforms.co.kr')
driver.implicitly_wait(3)

tag_names = driver.find_element_by_id("top-memu-wrap").find_elements_by_tag_name("a")

i = 1
print("******서식******")
for tag in tag_names:
    print(i,".", tag.text.split("\n"))
    i += 1

user_input = int(quote_plus(input('\n원하는 서식 번호를 입력해주세요: ')))

if user_input > len(tag_names) or user_input < 1:
    print("존재하지 않는 서식입니다. 다시 실행하여주세요")
    exit()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

for href in soup.select('#top-memu-wrap'):
    doctypeurl = href.findAll("a")[user_input - 1]['href'] # 0부터시작
    # //*[@id="top-memu-wrap"]/a[1]

url = f'http://freeforms.co.kr{doctypeurl}'

driver.get(url)

j = 0

try:  # 정상 처리
    ten = 0
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
    doc_list = []
    link = []
    pageNum = len(driver.find_element_by_tag_name("li").find_elements_by_class_name("page_box"))

    while True:
        if len(driver.find_elements_by_class_name("page_box_b")) == 0:
            # print(len(driver.find_element_by_tag_name("li").find_elements_by_class_name("page_box")))
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
            pageNum = len(driver.find_element_by_tag_name("ul").find_elements_by_class_name("page_box"))
            break
        element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
        pageNum = len(driver.find_element_by_tag_name("ul").find_elements_by_class_name("page_box"))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ten += 1
        url = url[:36] + str(ten * 10 + 1) + '.html' # ten = 6
        driver.get(url)
        pageNum = len(driver.find_element_by_tag_name("ul").find_elements_by_class_name("page_box"))
        if pageNum <=9:
            # print(len(driver.find_element_by_tag_name("li").find_elements_by_class_name("page_box")))
            for i in range(2 , len(driver.find_element_by_tag_name("li").find_elements_by_class_name("page_box"))):
                element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
                pageNum = len(driver.find_element_by_tag_name("ul").find_elements_by_class_name("page_box"))
                print("안녕", pageNum)
            break
        elif pageNum == 10 and len(driver.find_elements_by_class_name("page_box_b")) == 1:
            break
        else:
            continue


    print("총", ten * 10 + pageNum, "페이지 입니다.")
    driver.get(url[:36] + str(1) + '.html')
    print("현재 1 페이지 입니다.")

    for i in range(0, ten * 10 + pageNum):
        doc_data = driver.find_elements_by_class_name('title')
        download_data = len(driver.find_elements_by_class_name('contents_list-2'))
        webpage = requests.get(url[:36] + str(i+1) + '.html')
        soup = BeautifulSoup(webpage.content, "html.parser")

        for k in doc_data:
            doc_list.append(k.text.split('\n'))

        i = 0

        for href in soup.select(".contents_list-2"):
            new_url = "http://freeforms.co.kr" + href.find("a")["href"]
            link.append("http://freeforms.co.kr" + href.find("a")["href"])
            print(new_url)
            for name_href in soup.select(".contents_list"):
                # driver.get(new_url) # 다운
                # time.sleep(1) DDoS 방지용
                name = soup.select(".contents_list-1 > a")[i].text
                # // *[ @ id = "content"] / div[4] / div[1] / a
                # //*[@id="content"]/div[4]/div[2]/a
                print(i + 1,".", name,"다운로드 완료.")
                i += 1
                if (i >= 1):
                    break
            # //*[@id="content"]/div[4]/div[2]/a

        time.sleep(1)  # 웹페이지를 불러오기 위해 2초 정지

        if (j > ten * 10 + pageNum):
            break

        url = url[:36] + str(j+2) + '.html'
        driver.get(url)
        print("\n현재", j + 1, "페이지 다운로드를 마쳤습니다. \n")

        j += 1
        # //*[@id="content"]/div[6]/ul/a[1]

except TimeoutException:  # 예외 처리
    print('해당 페이지에 문서가 존재하지 않습니다.')

finally:  # 정상, 예외 둘 중 하나여도 반드시 실행
    driver.quit()

print("총 다운받은 문서의 개수:", len(doc_list))

doc_df = pd.DataFrame({'문서명': doc_list, 'URL': link})
doc_df = pd.DataFrame(zip(doc_list, link), columns=['문서명', 'URL'])
doc_df.index = doc_df.index + 1

doc_df.to_csv(f'doc_{user_input}_df.csv', mode='w', encoding='utf-8-sig',header=True, index=True)
print('웹 크롤링이 완료되었습니다.')