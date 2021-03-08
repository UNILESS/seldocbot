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

# Headless 크롬 옵션
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')

options.add_experimental_option("prefs", {
    "download.default_directory": r"C:/Users/sunup/Desktop/docdown",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(executable_path='C:/Users/sunup/PycharmProjects/seldocbot/chromedriver_win32/chromedriver.exe', options=options)
driver.get('http://freeforms.co.kr')
driver.implicitly_wait(3)



tag_names = driver.find_element_by_id("top-memu-wrap").find_elements_by_tag_name("a")
i = 1
for tag in tag_names:
    print(i,"번", tag.text.split("\n"))
    i += 1

user_input = int(quote_plus(input('\n원하는 서식 번호를 입력해주세요 : ')))

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

driver.get(url)


try:  # 정상 처리
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
    doc_list = []
    pageNum = len(driver.find_element_by_tag_name("li").find_elements_by_class_name("page_box"))
    print("총", pageNum, "페이지 입니다.")
    print("현재 1페이지 입니다.")

    j = 1

    for i in range(0, pageNum):
        doc_data = driver.find_elements_by_class_name('title') # 0
        download_data = len(driver.find_elements_by_class_name('contents_list-2'))
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, "html.parser")

        print(len(doc_data)) # 57개

        for k in doc_data:
            doc_list.append(k.text.split('\n'))


        num = 1
        i = 0
        for href in soup.select(".contents_list-2"):
            new_url = "http://freeforms.co.kr" + href.find("a")["href"]
            print(new_url)
            for name_href in soup.select(".contents_list"): # in 2
                # driver.execute_script("arguments[0].click();", go)
                # driver.find_element_by_xpath('//*[@id="content"]/div[4]/div[' + str(1 + j * 5) + ']/a/text()').extract()
                name = soup.select(".contents_list-1 > a")[i].text
                # // *[ @ id = "content"] / div[4] / div[1] / a
                # // *[ @ id = "content"] / div[4] / div[6] / a
                print(i + 1,".", name,"다운로드 완료.")
                i += 1
                if (i >= 1):
                    break
            # //*[@id="content"]/div[4]/div[2]/a

        time.sleep(2)  # 웹페이지를 불러오기 위해 2초 정지
        # //*[@id="content"]/div[6]/ul/a[1]
        j += 1

        if (j > pageNum):
            break

        if user_input == 1:
            url = "/form100/form_"+str(j)+".html"
        elif user_input == 2:
            url = "/form104/form_"+str(j)+".html"
        elif user_input == 3:
            url = "/form110/form_"+str(j)+".html"
        elif user_input == 4:
            url = "/form116/form_"+str(j)+".html"
        elif user_input == 5:
            url = "/form120/form_"+str(j)+".html"
        elif user_input == 6:
            url = "/form130/form_"+str(j)+".html"
        elif user_input == 7:
            url = "/form140/form_"+str(j)+".html"
        elif user_input == 8:
            url = "/form200/form_"+str(j)+".html"
        elif user_input == 9:
            url = "/form210/form_"+str(j)+".html"
        elif user_input == 10:
            url = "/form220/form_"+str(j)+".html"
        elif user_input == 11:
            url = "/form230/form_"+str(j)+".html"

        url = f'http://freeforms.co.kr{url}'
        driver.get(url)
        print("현재", j, "페이지 입니다.")

        # //*[@id="content"]/div[6]/ul/a[1]


except TimeoutException:  # 예외 처리
    print('해당 페이지에 문서가 존재하지 않습니다.')

finally:  # 정상, 예외 둘 중 하나여도 반드시 실행
    driver.quit()

print("doc_list : ", len(doc_list))

for i  in range(len(doc_list)):
    doc_list[i].append(doc_list[i][1])

doc_df = pd.DataFrame(doc_list, columns=['문서명', 'URL'])
doc_df.index = doc_df.index + 1

doc_df.to_csv(f'doc_{user_input}_df.csv', mode='w', encoding='utf-8-sig',header=True, index=True)
print('웹 크롤링이 완료되었습니다.')