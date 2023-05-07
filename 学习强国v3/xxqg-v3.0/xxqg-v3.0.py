# coding:utf-8

# 作者: 明明明明明白了
# 联系我：mmmmmbl@163.com
#
# 若chrome升级，请重新升级浏览器驱动
# http://chromedriver.storage.googleapis.com/index.html
# 在该网站查找对应win版本，解压到python解析器文件夹里：D:\develop\Python  -> 这个是自己安装python驱动的位置

# 打包方法： cd .\当前工作目录
# pyinstaller -F .\xxqg-v3.0.py  ⬅这个是要打包的文件夹名

# v3.0版本解决了：
#       1、更少量主动点击
#       2、用发送请求的方式避免了元素找不到、等待加载等等问题。
#       3、使用selenium的驱动获取cookies，第一次尝试（后续再试试用session记住请求，并获取cookies，哎太难了
#       4、结合读写，获取元素截图，便于扫码，并自动用完即刻删除。
#       5、可变变量抽离，更便于代码维护，拓展性增强


import json
import os
import time
from datetime import date, timedelta

import requests
from selenium.webdriver import Chrome
# 无头浏览器配置需要
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 需要配置的参数
myOptions = {
    # 在这填写电脑桌面位置，便于保存和删除图片
    "myDesktop": "E://桌面",
    # jkDY填写党员名单，jkFZDX填写发展对象名单，便于区分每日学习数量。可以通过这个来分组。一个人分在多组，则只判断jkDY！
    "jkDY": [
    # 这里是插件生成假数据，不是真人名！
    # 这里是填写自己支部下人员名单和其最低学习的分数……
        "卢强", "沈嘉怡", "毛雅涵", "董欣汝", "魏欣欣",
        "范佳惠", "余淑慧", "董淑华", "许嘉怡", "杨淑君",
        "冯欣源", "高杨", "曹欣慧", "朱淼", "毛佳琪",
        "万欣欣", "雷清妍", "曾瑞辰", "谭清妍", "梁冰洁"
    ],
    "jkFZDX": [],
    # rules里请保留Fail、rank1、rank2字段，用于统计不合格、良好、非常棒三个List
    # rank值为低于（<）,数组从上往下依次判断
    "DYrules": [
        {"name": "Fail", "rank": 40, "Tips": "不合格"},
        {"name": "Warn", "rank": 41, "Tips": "注意你很久了！不要每天40分咯"},
        {"name": "Default", "rank": 45, "Tips": "合格"},
        {"name": "Rank1", "rank": 50, "Tips": "Good！"},
        {"name": "Rank2", "rank": 100, "Tips": "你是怎么做到的！太强了"},
    ],
    "FZDXrules": [
        {"name": "Fail", "rank": 50, "Tips": "不合格"},
        {"name": "Default", "rank": 55, "Tips": "合格"},
        {"name": "Rank1", "rank": 60, "Tips": "Good！"},
        {"name": "Rank2", "rank": 100, "Tips": "你是怎么做到的！太强了"},
    ],
    # 输出模板，每次携带，方便来复制。。。整个顶头写，文字包在”“”XXX“”“”中间，方便可以可以换行输出
    "printRuleTips": """
-------【备用模板】--------------------"
备用模板/备用模板/备用模板/备用模板/备用模板/备用模板/备用模板/备用模板/备用模板
可以在这里留存你的备用模板，比如经常可能会到的话，便于来复制。
推荐定格写，这样输出时也是相对于命令行定格的，利于查看、复制等等。。。。
你也可以在这里使用\n来换行输入！
    """
}


# 最后输出的函数
def printResult(Lists):
    tplt = "{0:^4}\t{1:^4}\t{2:^8}\t{3:^8}\t{4:^8}\t{5:^8}\t{6:<8}"
    print(tplt.format("序号", "姓名", "年度积分", "昨日积分", "当月积分", "总积分", "备注", chr(12288)))
    idx = 1
    for i in Lists:
        print(tplt.format(idx, i[0], i[1], i[2], i[3], i[4], i[5], chr(12288)))
        idx = idx + 1
# 等待点击的函数
def WaitClick(xpath, msg=''):
    # 该函数循环寻找对应xpath，找到并点击
    # 传参可选输出，运行注释用，不传默认不输出
    so = web.find_elements(By.XPATH, xpath)
    while not so:
        time.sleep(1)
        so = web.find_elements(By.XPATH, xpath)
    time.sleep(1)
    so[0].click()
    if msg:
        print(msg)
    return so[0]
# 删除图片的函数
def deletePNG(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print('成功删除文件:', file_name)
    else:
        print('未找到此文件:', file_name)
# 根据分数，分组加入对应的List
def AddList(name, strName):
    if strName == "Fail":
        FailList.append(name)
    elif strName == "Rank1":
        Rank1List.append(name)
    elif strName == "Rank2":
        Rank2List.append(name)
# 判断规则，返回notes信息
def studyRules(name, rank):
    jkDY = myOptions['jkDY']
    DYrules = myOptions['DYrules']
    jkFZDX = myOptions['jkFZDX']
    FZDXrules = myOptions['FZDXrules']

    if name in jkDY:  # 是党员
        for i in range(0, len(DYrules)):
            if DYrules[i]['rank'] > rank:
                AddList(name, DYrules[i]['name'])
                return DYrules[i]['Tips']
    elif name in jkFZDX:
        for i in range(0, len(FZDXrules)):
            if FZDXrules[i]['rank'] > rank:
                AddList(name, DYrules[i]['name'])
                return FZDXrules[i]['Tips']
    else:
        return "该同志还不在系统中，请联系管理员添加信息"
# 输出总结
def printConclusion():
    print(f"【学习强国{today.__format__('%Y年%m月%d日')}学习情况总结】")
    idx = 1
    if len(FailList) > 0:
        if len(FailList) > 1:
            print(f"1、昨日未完成学习的同志共{len(FailList)}位，分别是{FailList}")
        else:
            print(f"1、昨日未完成学习的同志共{len(FailList)}位，他是{FailList}")
    else:
        print("1、昨日所有同志都完成的了学习！请大家继续保持。")
    if len(Rank1List) > 0:
        idx = idx + 1
        if len(Rank1List) > 1:
            print(f"{idx}、昨日的完成良好的同志共{len(Rank1List)}位，分别是{Rank1List}")
        else:
            print(f"{idx}、昨日的完成良好的同志共{len(Rank1List)}位，他是{Rank1List}")
    if len(Rank2List) > 0:
        idx = idx + 1
        if len(Rank2List) > 1:
            print(f"{idx}、昨日特别表扬的同志共{len(Rank2List)}位，分别是{Rank2List}，请其他同志向他们学习！")
        else:
            print(f"{idx}、昨日特别表扬的同志共{len(Rank2List)}位，他是{Rank2List}，请其他同志向他学习！")
    print()
# 输出可复制的结论
def printCopy():
    print("\n------------------------------------------------------------------------------")
    print(f"【学习强国{today.__format__('%Y年%m月%d日')}学习情况总结】")
    if len(FailList) > 0:
        if len(FailList) > 1:
            print(f"1、昨日未完成学习的同志共{len(FailList)}位，分别是{FailList}")
        else:
            print(f"1、昨日未完成学习的同志共{len(FailList)}位，他是{FailList}")
    else:
        print("1、昨日所有同志都完成的了学习！请大家继续保持。")
    print("2、昨日未上传感想的同志：（迟交1天）")
    if len(Rank2List) > 0:
        if len(Rank2List) > 1:
            print(f"2、今天特别表扬以下这{len(Rank2List)}位同志，他们分别是{Rank2List}，请其他同志向他们学习！")
        else:
            print(f"2、今天特别表扬{Rank2List}同志，请其他同志向他学习！")
    print("学而时习之，不亦说乎！~~~大家继续加油！")
# 输出自己的规则，以便随时取用
def printRuleTips():
    print(myOptions['printRuleTips'])
    print("\n------------------------------------------------------------------------------")


opt = Options()
# 如果想要页面无法察觉到你是自动的程序，可以这样写，让浏览器的window.navigator=false
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
opt.add_argument("--disable-blink-features=AutomationControlled")

web = Chrome(options=opt)
web.implicitly_wait(2)
url = "https://login.xuexi.cn/login"
web.get(url)

# 格式化日期
today = date.today()
yesterday = today + timedelta(days=-1)
todaySTR = today.__format__('%Y%m%d')
yesterdaySTR = yesterday.__format__('%Y%m%d')

# 保存图片
img_save = WaitClick('//*[@id="root"]/div[1]/div')
imgfilesName = f"{myOptions['myDesktop']}//学习强国扫码{todaySTR}.png"
screenshotPNG = img_save.screenshot_as_png  # 截取后直接是二进制,无括号
with open(imgfilesName, mode="wb") as f:
    f.write(screenshotPNG)

# 进入按钮
print(f"请去桌面对应日期图片扫码，图片不用手动删除，默认会在结束进程后自动删除。。。")
print("-------------")
WaitClick('//*[@id="root"]/div[1]/div/div[2]/form/div/div/div/span/button', "扫码成功!")
deletePNG(imgfilesName)  # 此时图片没用了，删除即可！
time.sleep(2)

# 获取cookies
cookie_dict = {}
cookie_list = web.get_cookies()  # 获取cookies
for cookie in cookie_list:
    cookie_dict[cookie['name']] = cookie['value']

# 请求URL、请求头、请求body参数
getDataReq = "https://odrp.xuexi.cn/report/commonReport"
headers = {
    "Cookie": f"csrf_token={cookie_dict['csrf_token']}; token_={cookie_dict['token_']}",
    "Referer": "https://study.xuexi.cn/",
    "Content-Type": "application/json",
}
data = {
    "apiCode": "ab4afc14",
    "dataMap": {
        "startDate": yesterdaySTR,
        "endDate": yesterdaySTR,
        "offset": 0,
        "sort": "rangeRealScore",
        "pageSize": 200,
        "order": "asc",
        "isActivate": "",
        "orgGrayId": "m91K4Ym3wtZLTJpglVIC5Q=="
    }
}
# 发出请求并判断失败与否
res = requests.post(getDataReq, headers=headers, data=json.dumps(data))
code = json.loads(res.text)['code']  # 获取请求的code，用于判断请求的成功
if code >= 300:
    print("token过期了，或其他错误。请排查后重试……")
    exit()

# 数据整理
OKUseData = json.loads(json.loads(res.text)['data_str'])['dataList']
peopleCount = OKUseData['count']  # 人员总数
peopleDatas = OKUseData['data']
showList = []
FailList = []
Rank1List = []
Rank2List = []
for p in peopleDatas:
    userName = p['userName']  # 用户名
    userId = p['userId']  # 用户id
    isActivate = p['isActivate']  # 活跃状态
    rangeRealScore = p['rangeRealScore']  # 计入年度积分
    rangeScore = p['rangeScore']  # 计入总积分
    scoreMonth = int(p['scoreMonth'] / 1000)  # 当月积分
    totalScore = p['totalScore']  # 年度总积分
    notes = studyRules(userName, rangeRealScore)  # 备注
    showList.append([userName, rangeRealScore, rangeScore, scoreMonth, totalScore, notes])

# 这里还能对showList进行再加工……

# 输出数据并结束进程
printRuleTips()
printResult(showList)
printConclusion()
printCopy()
web.close()
