# coding=utf-8
import requests
import base64
import rsa
import time
from bs4 import BeautifulSoup as bs

try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename = 'cookie.txt')
username = '学号'
mm = b'密码'
url='http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html'

#定义的header
header1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Content-Length": "462",
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "JSESSIONID=C6299565CC01CDA3B180BAB0208D9C5B",
            "Host": "jwxt.neuq.edu.cn",
            "Origin": "http://jwxt.neuq.edu.cn",
            "Proxy-Connection": "keep-alive",
            # "Referer": "http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36",
        }


#获取csrf_token，该值为表单中必须的
def get_csrf_token():
    page = session.get(url)
    soup = bs(page.text, "html.parser")
    # 获取认证口令csrftoken
    csrftoken = soup.find(id="csrftoken").get("value")
    return csrftoken


#从公钥接口获取到构造公钥的模和指数，并在本地生成公钥对明文密码加密。
def get_passwd():
    publickey = session.get('http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_getPublicKey.html').json()
    b_modulus = base64.b64decode(publickey['modulus'])  # 将base64解码转为bytes
    b_exponent = base64.b64decode(publickey['exponent'])  # 将base64解码转为bytes
    # 公钥生成,python3从bytes中获取int:int.from_bytes(bstring,'big')
    modulus = int.from_bytes(b_modulus, 'big')
    exponent = int.from_bytes(b_exponent, 'big')
    mm_key = rsa.PublicKey(modulus, exponent)
    # 利用公钥加密,bytes转为base64编码
    passwd = base64.b64encode(rsa.encrypt(mm, mm_key))
    return passwd


#提交登录表单，并利用cookiejar保存cookie
def parse():
    payload = {
        'csrftoken': get_csrf_token(),
        'yhm': username,
        'mm': get_passwd()
    }
    r = session.post(url, data=payload, headers=header1)
    cookies = session.cookies
    cookies.save(ignore_discard=True, ignore_expires=True)
    # print(cookies)
    print('新的Cookie是'+r.request.headers['Cookie'])

    
#登录主体函数
def login():
    try:
        session.cookies.load(ignore_discard = True)
        url = 'http://jwxt.neuq.edu.cn/jwglxt/xtgl/index_initMenu.html'
        statue = session.get(url=url, allow_redirects=False).status_code
        old_cookie = session.get(url=url).request.headers['Cookie']
        if(statue == 200):
            print('登陆成功！')
            print('此时的cookie是', old_cookie)
        else:
            print('cookie过期，重新登录')
            parse()

    except:
        print('未能加载cookie')
        parse()

        
#通过提交查询信息根据返回的json获取成绩（2018年上学期）
def get_grade():
    url = 'http://jwxt.neuq.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
    data = {
        'xnm': '2018',
        'xqm': '',
        '_serach': 'false',
        'nd': int(time.time()),
        'queryModel.showCount': '10',
        'queryModel.currentPage': '1',
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': ''
    }
    results = session.post(url=url, data=data, headers=header1).json()
    # print('成绩是',results['items'][0]['cj'])
    # print('学分是',results['items'][0]['xf'])
    # print('成绩是',results['items'][1]['cj'])
    # print('学分是',results['items'][1]['xf'])
    # print(results.text)

    
#获取课表（2018年上学期的课程）
def get_class():
    xskb_url = 'http://jwxt.neuq.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
    xskb_data = {
        'xnm': '2018',
        'xqm': '3'
    }
    syk_url = 'http://jwxt.neuq.edu.cn/jwglxt/xssygl/sykbcx_cxSykbcxxsIndex.html?doType=query&gnmkdm=N253508'
    syk_data = {
        'xnm': '2018',
        'xqm': '3',
        '_search': 'false',
        'nd': int(time.time()),
        'queryModel.showCount': '30',
        'queryModel.currentPage': '1',
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': ''
    }
    xskb_results = session.post(url=xskb_url, data=xskb_data, headers=header1).json()
    print('课表如下')
    for i in xskb_results["kbList"]:
        print(i['cdmc'], i['jc'], i['kcmc'], i['khfsmc'], i['xm'], i['xqjmc'], i['zcd'])
    print('实践课如下')
    for i in xskb_results["sjkList"]:
        print(i['kcmc'], i['qsjsz'], i['xm'])

    syk_result = session.post(url=syk_url, data=syk_data, headers=header1).json()
    print('实验课如下')
    for i in syk_result["items"]:
        print(i['jsxm'], i['kcmc'], i['syfj'], i['syfzmc'], i['xmmc'], i['xqjmc'], i['zcd'])



login()
get_grade()
get_class()



