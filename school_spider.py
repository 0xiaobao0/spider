from selenium import webdriver
import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
session = requests.session()


def get_cookie():
    driver.get('http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html')
    driver.find_element_by_id('yhm').send_keys('20168709')
    driver.find_element_by_id('mm').send_keys('123abc')
    driver.find_element_by_id('dl').click()
    cook = driver.get_cookies()
    for item in cook:
        cookie = item['name'] + '=' + item['value']
    return cookie


def get_score(cookie):
    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    driver.get('http://jwxt.neuq.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=20168709')
    driver.find_element_by_id('xnm').send_keys('')
    driver.find_element_by_id('xqm').send_keys('')
    driver.find_element_by_id('search_go').click()
    # url = 'http://jwxt.neuq.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=20168709'
    # r = session.get(url, headers=headers)
    # return r.text

# 这个函数是很久之前刚学python写的了，很丑陋，不过拿到成绩后怎么分析就可以随便写了。
def analyse(text):
    json_dict = json.loads(text, encoding="utf-8")
    json_cj = json_dict['items']
    a = 0
    for cj in json_cj:
        cjj = cj['bfzcj']
        cjj = int(cjj)
        if cjj >= 60:
            print('学科名称:', cj['kcmc'], ' ', '成绩:', cj['bfzcj'])
            a += 1
    print('共计', a, '门学科')
    print(' ')
    for cj in json_cj:
        cjj = cj['bfzcj']
        cjj = int(cjj)
        if cjj < 60:
            print('挂科科目', cj['kcmc'], '挂科成绩', cj['bfzcj'])


if __name__ == '__main__':
    cookie = get_cookie()
    print(get_score(cookie))
    # analyse(text)
    # driver.quit()
# print(get_cookie())