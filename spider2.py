from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import requests
from IdMap import IdMap


doc_id_map = IdMap()  # doc to id
url_id_map = IdMap()  # url to id


url_anc_map = {}  # url to anctext
url_list_map = {}  # page link info


def set_sleep_time( t):
    time.sleep( t)

By.xpath



s = Service(r"C:/Users/nan/Desktop/Web_Search_Engine/chromedriver.exe")
driver = webdriver.Chrome(service=s)

#driver.maximize_window()

# 要爬取的网页
neirongs = []  # 网页内容
response = []  # 网页数据
travel_urls = []
urls = []
titles = []
writefile = open("docs.txt", 'w', encoding='UTF-8')
url = 'http://travel.yunnan.cn/yjgl/index.shtml'
#url = 'http://cc.nankai.edu.cn'
# 第一页
driver.get(url)
#print(driver.page_source)

response.append(driver.page_source)
# 休息时间
set_sleep_time(3)


# 第二页的网页数据
# browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
# s(3)
# response.append(browser.page_source)
# s(3)

# 第三页的网页数据
# browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
# s(3)
# response.append(browser.page_source)



# 3.用正则表达式来删选数据
reg = r'href="(//travel.yunnan.cn/system.*?)"'
# 从数据里爬取data。。。
# 。travel_urls 旅游信息网址
for i in range(len(response)):
    travel_urls = re.findall(reg, response[i])

print(travel_urls)
# 打印出来放在一个列表里
for i in range(len(travel_urls)):
    url1 = 'http:' + travel_urls[i]
    urls.append(url1)
    driver.get(url1)
    content = driver.find_element("xpath",'/html/body/div[7]/div[1]/div[3]').text
    # 获取标题作为文件名
    b = driver.page_source
    travel_name = driver.find_element("xpath",'//*[@id="layer213"]').text
    titles.append(travel_name)
print(1)
print(titles)
print(urls)
for j in range(len(titles)):
    writefile.write(str(j) + '\t\t' + titles[j] + '\t\t' + str(urls[j]) + '\n')

set_sleep_time(1)


driver.close()



'''
# 模拟浏览器，使用谷歌浏览器，将chromedriver.exe复制到谷歌浏览器的文件夹内
chromedriver = r"C:/Users/nan/Desktop/Web_Search_Engine/chromedriver.exe"

# 设置浏览器
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(executable_path=chromedriver)

# 最大化窗口 用不用都行
browser.maximize_window()

# 要爬取的网页
neirongs = []  # 网页内容
response = []  # 网页数据
travel_urls = []
urls = []
titles = []
writefile = open("docs.txt", 'w', encoding='UTF-8')
url = 'http://travel.yunnan.cn/yjgl/index.shtml'
# 第一页
browser.get(url)
response.append(browser.page_source)
# 休息时间
set_sleep_time(3)

# 第二页的网页数据
# browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
# s(3)
# response.append(browser.page_source)
# s(3)

# 第三页的网页数据
# browser.find_element_by_xpath('// *[ @ id = "downpage"]').click()
# s(3)
# response.append(browser.page_source)

# 3.用正则表达式来删选数据
reg = r'href="(//travel.yunnan.cn/system.*?)"'
# 从数据里爬取data。。。
# 。travel_urls 旅游信息网址
for i in range(len(response)):
    travel_urls = re.findall(reg, response[i])

# 打印出来放在一个列表里
for i in range(len(travel_urls)):
    url1 = 'http:' + travel_urls[i]
    urls.append(url1)
    browser.get(url1)
    content = browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[3]').text
    # 获取标题作为文件名
    b = browser.page_source
    travel_name = browser.find_element_by_xpath('//*[@id="layer213"]').text
    titles.append(travel_name)
print(titles)
print(urls)
for j in range(len(titles)):
    writefile.write(str(j) + '\t\t' + titles[j] + '\t\t' + str(urls[j]) + '\n')

set_sleep_time(1)
browser.close()
'''