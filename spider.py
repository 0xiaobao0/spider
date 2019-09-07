# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/8/31 20:45'

import requests
import base64
import rsa
import time
import re
import db
import datetime


from bs4 import BeautifulSoup as bs

try:
    import cookielib
except:
    import http.cookiejar as cookielib



session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename = 'cookie.txt')
url='http://jwxt.neuq.edu.cn/jwglxt/xtgl/login_slogin.html'
database = db.db()

def save_page(text):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open(file=now_time + '.txt', mode='w') as file:
        file.write(text)


def get_current_week():
    import time
    # 开学时间，手动维护
    start_year, start_month, start_day = 2019, 8, 26

    now_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    now_time = now_time.split(".")
    now_year, now_month, now_day = eval(now_time[0]), eval(now_time[1].strip("0")), eval(now_time[2].lstrip("0"))

    if (now_year % 400 == 0) or (now_year % 4 == 0 and now_year % 100 != 0):
        month_year = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        month_year = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if start_year == now_year:
        if now_month > start_month:
            already_day = (month_year[start_month] - start_day) + sum(month_year[start_month + 1:now_month]) + now_day
        else:
            already_day = (month_year[start_month] - start_day)
        result_week = (already_day // 7) + 1
    else:
        # 上一年总天数
        last_yearday = month_year[start_month] - start_day + sum(month_year[start_month + 1:])
        now_yearday = sum(month_year[0:now_month]) + now_day
        result_week = (last_yearday + now_yearday) // 7 + 1

    return result_week

#定义的header
header1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Content-Length": "462",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "jwxt.neuq.edu.cn",
            "Origin": "http://jwxt.neuq.edu.cn",
            "Proxy-Connection": "keep-alive",
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
    mm = bytes(input('请输入密码：'), encoding='utf-8')
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
    username = input('请输入用户名：')
    payload = {
        'csrftoken': get_csrf_token(),
        'yhm': username,
        'mm': get_passwd()
    }
    r = session.post(url, data=payload, headers=header1)
    test_login_url = 'http://jwxt.neuq.edu.cn/jwglxt/xtgl/index_initMenu.html'
    response = session.get(url=test_login_url, allow_redirects=False)
    statue = response.status_code
    if (statue == 200):
        print('登陆成功！')
        cookies = session.cookies
        cookies.save(ignore_discard=True, ignore_expires=True)
        print('新的Cookie是' + r.request.headers['Cookie'])
    else:
        print('用户名密码错误！')
        print('请重新输入用户名密码')
        parse()



#登录主体函数
def login():
    try:
        session.cookies.load(ignore_discard = True)
        url = 'http://jwxt.neuq.edu.cn/jwglxt/xtgl/index_initMenu.html'
        res = session.get(url=url, allow_redirects=False)
        statue = res.status_code
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


# 通过提交查询信息根据返回的json获取成绩（2018年上学期）
def get_grade():
    url = 'http://jwxt.neuq.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
    year = input('请输入需要查询的学年：')
    semester = input('请输入需要查询的学期：')
    if int(semester) == 1:
        semester = 3
    if int(semester) == 2:
        semester = 12
    data = {
        'xnm': year,
        'xqm': semester,
        '_serach': 'false',
        'nd': int(time.time()),
        'queryModel.showCount': '10',
        'queryModel.currentPage': '1',
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': ''
    }
    res = session.post(url=url, data=data)
    save_page(res.text)
    results = res.json()
    res_list = []
    year = int(year)
    semester = int(semester)
    for i in results['items']:
        res_dic = {}
        res_dic['kcmc'] = i['kcmc']
        res_dic['ksxz'] = i['ksxz']
        res_dic['cj'] = str(i['cj'])
        res_list.append(res_dic)
        sql = 'insert into student_grade (class_name, class_type, grade, year, term) values("{}", "{}", "{}", "{}", "{}")'.format(res_dic["kcmc"], res_dic["ksxz"], res_dic["cj"], year, semester)
        res = database.excute(sql)
        print(res_dic)
        if res == None:
            print('成功插入一条成绩记录！')
    # print(res_list)
    select_function()


# 获取课表（2018年上学期的课程）
def get_class():
    classList = []
    num_dict = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7}
    xskb_url = 'http://jwxt.neuq.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
    year = input('请输入需要查询的学年：')
    semester = input('请输入需要查询的学期：')
    if int(semester) == 1:
        semester = 3
    if int(semester) == 2:
        semester = 12
    xskb_data = {
        'xnm': year,
        'xqm': semester
    }
    res = session.post(xskb_url, data=xskb_data, headers=header1)
    save_page(res.text)
    xskb_results = res.json()
    print('课表获取成功')
    for i in xskb_results["kbList"]:
        classObj = {}
        class_range = [int(i) for i in re.findall(r'\d+', i['jc'])]
        week_range = []
        str_week_range = [i for i in re.findall(r'\d+\-?\d*', i['zcd'])]
        for j in str_week_range:
            rangelist = [int(n) for n in re.findall(r'\d+', j)]
            week_range.append(rangelist)
        kcmc = i['kcmc'] + '@' + i['cdmc']
        classObj['week_day'] = num_dict[i['xqjmc']]
        classObj['start_section'] = class_range[0]
        classObj['section_number'] = class_range[1] - class_range[0] + 1
        classObj['class_name'] = kcmc
        classObj['week_range'] = week_range
        classObj['teacher'] = i['xm']
        classObj['test_type'] = i['khfsmc']
        classList.append(classObj)
        sql = 'insert into class (class_name, week_day, start_section, section_num, week_range, teacher, test_type, year, term) values("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            classObj["class_name"], classObj["week_day"], classObj["start_section"], classObj["section_number"], classObj["week_range"], classObj["teacher"], classObj["test_type"], year, semester)
        res = database.excute(sql)
        print(res)
        print(classObj)
        if res == None:
            print('成功插入一条成绩记录！')
    print(classList)
    select_function()

def get_practice_class():
    classdesign = []
    xskb_url = 'http://jwxt.neuq.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508'
    year = input('请输入需要查询的学年：')
    semester = input('请输入需要查询的学期：')
    if int(semester) == 1:
        semester = 3
    if int(semester) == 2:
        semester = 12
    xskb_data = {
        'xnm': year,
        'xqm': semester
    }
    res = session.post(xskb_url, data=xskb_data, headers=header1)
    save_page(res.text)
    xskb_results = res.json()
    print('获取实践课成功！')
    for i in xskb_results["sjkList"]:
        classdesignObj = {}
        classdesignObj['class_name'] = i['kcmc']
        classdesignObj['week_range'] = i['qsjsz']
        classdesignObj['teacher'] = i['xm']
        classdesign.append(classdesignObj)
        print(classdesignObj)
    # print(classdesign)
    # print(i['kcmc'], i['qsjsz'], i['xm'])
    select_function()

def get_experiment():
    classList = []
    num_dict = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7}
    syk_url = 'http://jwxt.neuq.edu.cn/jwglxt/xssygl/sykbcx_cxSykbcxxsIndex.html?doType=query&gnmkdm=N253508'
    year = input('请输入需要查询的学年：')
    semester = input('请输入需要查询的学期：')
    if int(semester) == 1:
        semester = 3
    if int(semester) == 2:
        semester = 12
    syk_data = {
        'xnm': year,
        'xqm': semester
    }
    res = session.post(syk_url, data=syk_data, headers=header1)
    save_page(res.text)
    syk_result = res.json()
    print('获取实验课表成功！')
    for i in syk_result["items"]:
        classObj = {}
        class_range = [int(i) for i in re.findall(r'\d+', i['jc'])]
        week_range = []
        str_week_range = [i for i in re.findall(r'\d+\-?\d*', i['zcd'])]
        for j in str_week_range:
            rangelist = [int(n) for n in re.findall(r'\d+', j)]
            week_range.append(rangelist)
        kcmc = i['kcmc'] + '@' + i['syfj'].split("/")[0]
        classObj['xqj'] = num_dict[i['xqjmc']]
        classObj['skjc'] = class_range[0]
        classObj['skcd'] = class_range[1] - class_range[0] + 1
        classObj['kcmc'] = kcmc
        classObj['week_range'] = week_range
        classObj['teacher'] = i['jsxm']
        classObj['symc'] = i['xmmc']
        classList.append(classObj)
        print(classObj)
    # print(classList)
    select_function()

def get_empty_class_room():
    import json
    week = input('请输入查询的周：').split(' ')
    day = input('请输入星期几：').split(' ')
    characters = input('请输入第几节课：').split(' ')
    # print(week, day, characters)
    page = input('请输入页数:')
    week_data = str(sum([pow(2, int(i) - 1) for i in week]))
    day_data = ','.join([str(int(i)) for i in day])
    characters_data = str(sum([pow(2, int(i) - 1) for i in characters]))
    # print(week_data, day_data, characters_data)
    emptyClassroomList = []
    query_url = 'http://jwxt.neuq.edu.cn/jwglxt/cdjy/cdjy_cxKxcdlb.html?doType=query&gnmkdm=N2155'
    query_data = {
        'fwzt': 'cx',
        'xnm': '2019',
        'xqm': '3',
        'zcd': week_data,
        'xqj': day_data,
        'jcd': characters_data,
        'jyfs': '0',
        'xqh_id': '3D669E6DAB06A186E053AB14CECA64B4',
        'queryModel.showCount': '15',
        'queryModel.currentPage': str(page),
        'queryModel.sortName': 'cdbh',
        'queryModel.sortOrder': 'asc'
    }
    res = session.post(query_url, data=query_data, headers=header1)
    save_page(res.text)
    query_result = res.json()
    print('获取空教室成功')
    for i in query_result["items"]:
        emptyClassroomObj = {}
        emptyClassroomObj['cdmc'] = i['cdmc']  # 场地名称
        emptyClassroomObj['xqmc'] = i['xqmc']  # 校区
        emptyClassroomObj['jxlmc'] = i['jxlmc']  # 楼号
        emptyClassroomObj['zws'] = i['zws']  # 座位数
        emptyClassroomObj['lch'] = i['lch']  # 楼层号
        emptyClassroomObj['cdlbmc'] = i['cdlbmc']  # 场地类别
        emptyClassroomList.append(emptyClassroomObj)
        print(emptyClassroomObj)
    # print(emptyClassroomList)
    select_function()

def select_function():
    print('功能选择：1=>获取成绩  2=>获取课表  3=>获取实践课 ')
    print('          4=>获取实验  5=>获取空教室')
    func = input('请输入您的选择：')
    if func == '1':
        get_grade()
    if func == '2':
        get_class()
    if func == '3':
        get_practice_class()
    if func == '4':
        get_experiment()
    if func == '5':
        get_empty_class_room()

def main():
    login()
    select_function()

if __name__ == '__main__':
    main()