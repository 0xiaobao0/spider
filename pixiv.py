import requests
url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
sesssion = requests.session()
from bs4 import BeautifulSoup as bs
from lxml import etree

header1 = {
            "Origin": "https://accounts.pixiv.net",
            "Proxy-Connection": "keep-alive",
            "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36",
        }

def get_post_key():
    page = sesssion.get(url)
    soup = bs(page.text,'html.parser')
    post_key = soup.find_all('input')[0].get('value')
    return post_key

def login():
    payload = {
        'pixiv_id': '1920566573@qq.com',
        # 'captcha': '',
        # 'g_recaptcha_response': '',
        'password': '19970827lbb',
        'post_key': get_post_key(),
        # 'source': 'pc',
        # 'ref': 'wwwtop_accounts_index',
        # 'return_to': 'https://www.pixiv.net/'
    }
    r = sesssion.post(url=url, data=payload, headers=header1)


def follow_page():
    url = 'https://www.pixiv.net'
    r = sesssion.get(url=url, headers=header1)
    response = etree.HTML(r.text)
    page_tag = response.xpath('//*[@id="modal-mymenu"]/div/div[2]/a[1]')
    # ass = etree.tostring(page_url[0], encoding='utf-8', pretty_print=False, method='html')
    page_url = 'https://www.pixiv.net/bookmark.php?id=27415362&type=user'
    r2 = sesssion.get(url=page_url, headers=header1)
    print(r2.text)


login()
follow_page()