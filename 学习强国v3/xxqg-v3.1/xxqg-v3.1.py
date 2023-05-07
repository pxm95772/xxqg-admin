# coding:utf-8

# 作者: 明明明明明白了
# 联系我：mmmmmbl@163.com
#
# 若chrome升级，请重新升级浏览器驱动
# http://chromedriver.storage.googleapis.com/index.html
# 在该网站查找对应win版本，解压到python解析器文件夹里：D:\develop\Python

# 打包方法： cd .\
# pyinstaller -F .\xxqg-v3.1.py  ⬅这个是要打包的文件夹名字

# v3.1版本解决了：
# 1、项目可配置的参数放入配置文件config.yaml中，随时可以修改，便于更大限度自定义地查询。
# 2、利用updateConfig.py文件修改yaml配置文件，便于不熟悉yaml文件语法的同学修改配置文件，以免出面出现缩进、语法等不正确而导致读取配置失败或资源结构错误。
# 3、注重代码结构，项目函数再次封装，更多细节的变化。
# 4、引入捕捉报错模块，若有错，每次都可以看到报错说明。
# 5、试图解决部分设备程序结束，控制台自动关闭问题，添加等待输入结束，可以通过关闭页面或Ctrl+C关闭程序。


import json
import os
import time
from datetime import date, timedelta

import requests
import yaml
from selenium.webdriver import Chrome
# 无头浏览器配置需要
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

yamlPath = "./config.yaml"
XXQG_URL = "https://study.xuexi.cn/"
XXQG_Login_URL = "https://login.xuexi.cn/login"
getDataRequest = "https://odrp.xuexi.cn/report/commonReport"
zrSTR = ""
EQCodeImg_xpath = '//*[@id="root"]/div[1]/div'
ButtonLogin_xpath = '//*[@id="root"]/div[1]/div/div[2]/form/div/div/div/span/button'


# ---------工具相关
# 等待退出
def EscQuit():
    input("请按任意键退出…………")
    exit()

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

# 格式化日期
def DateFormat(Date, str):
    return Date.__format__(str)

# ---------业务相关
# 读取文件函数，并将文件还原成对象返回
def readConfigFile(FilePath):
    try:
        with open(FilePath, 'r', encoding='utf-8') as f:
            content = yaml.load(f.read(), Loader=yaml.FullLoader)
    except Exception as err:
        print(f"该文件（{FilePath}）找不到，请将文件放在正确位置后再进行操做！")
        print(f"错误原因：{err}")
        EscQuit()
    return content

# 获取web驱动
def getWebObject():
    opt = Options()
    # 如果想要页面无法察觉到你是自动的程序，可以这样写，让浏览器的window.navigator=false
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_argument("--disable-blink-features=AutomationControlled")
    webDriver = Chrome(options=opt)
    webDriver.implicitly_wait(2)
    return webDriver

# 获取要查询的日期
def getDate(DataDate):
    if type(DataDate) == int:
        if DataDate >= 1:
            print("无法查询今天及未来的数据！前一天数据至少等到第二天7点即可查询")
            EscQuit()

        # 很无聊的全局变量，判断是否是昨日
        global zrSTR
        if DataDate == -1:
            zrSTR = "昨日"

        select_day = today + timedelta(days=DataDate)
    elif type(DataDate) == str:
        print("DataDate暂不支持字符串/日期类型")
        EscQuit()
    else:
        print("DataDate暂不支持该类型数据查询……")
        EscQuit()
    return select_day

# 保存二维码
def saveQRCode():
    img_save = WaitClick(EQCodeImg_xpath)
    img_files_name = f"{myDesktop}//学习强国扫码{SelectDaySTR}.png"
    screenshotPNG = img_save.screenshot_as_png  # 截取后直接是二进制,无括号
    with open(img_files_name, mode="wb") as f:
        f.write(screenshotPNG)
    print(f"请去桌面[{myDesktop}]对应日期图片扫码，图片可以不用手动删除，默认会在扫码完成后自动删除。。。")
    print("-----------------------------------")
    return img_files_name

# 删除图片的函数
def deletePNG(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print('成功删除文件:', file_name)
    else:
        print('未找到或已经删除了此文件:', file_name)

# 发出请求，返回相应的数据
def sendRequest(cookie_dict, org_grayId, startDate, endDate):
    headers = {
        "Cookie": f"csrf_token={cookie_dict['csrf_token']}; token_={cookie_dict['token_']}",
        "Referer": XXQG_URL,
        "Content-Type": "application/json",
    }
    RequestData = {
        "apiCode": "ab4afc14",
        "dataMap": {
            "startDate": startDate,
            "endDate": endDate,
            "offset": 0,
            "sort": "rangeRealScore",
            "pageSize": 200,
            "order": "asc",
            "isActivate": "",
            "orgGrayId": org_grayId
        }
    }
    res = requests.post(getDataRequest, headers=headers, data=json.dumps(RequestData))
    res_json = json.loads(res.text)
    if res_json['code'] >= 300:
        print("token过期了，或其他错误。请排查后重试……")
        EscQuit()
    return res_json

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
    StudyGroup = myConfig['StudyGroup']
    for item in StudyGroup:
        group = StudyGroup[item]
        peopleList = group['People']
        ruleList = group['Rules']
        if name in peopleList:
            for i in range(len(ruleList)):
                if ruleList[i]['rank'] > rank:
                    AddList(name, ruleList[i]['name'])
                    return ruleList[i]['Tips']
    else:
        return myConfig['NotFindTips']

# 输出总结
def printConclusion(CopyBestPeople, CopyAllPeopleOK):
    print(f"【学习强国{DateFormat(SelectDay, '%Y年%m月%d日')}学习情况总结】")
    idx = 1

    if len(FailList) > 0:
        if len(FailList) > 1:
            print(f"1、{zrSTR}未完成学习的同志共{len(FailList)}位，分别是{FailList}")
        else:
            print(f"1、{zrSTR}未完成学习的同志共{len(FailList)}位，他是{FailList}")
    else:
        print(f"1、{CopyAllPeopleOK}")

    if len(Rank1List) > 0:
        idx = idx + 1
        if len(Rank1List) > 1:
            print(f"{idx}、{zrSTR}完成良好的同志共{len(Rank1List)}位，分别是{Rank1List}")
        else:
            print(f"{idx}、{zrSTR}完成良好的同志共{len(Rank1List)}位，他是{Rank1List}")
    if len(Rank2List) > 0:
        idx = idx + 1
        if len(Rank2List) > 1:
            print(f"{idx}、{zrSTR}特别表扬的同志共{len(Rank2List)}位，分别是{Rank2List}，{CopyBestPeople}")
        else:
            print(f"{idx}、{zrSTR}特别表扬的同志共{len(Rank2List)}位，他是{Rank2List}，{CopyBestPeople}")
    print("\n")

# 输出可复制的结论
def printCopy(CopyBestPeople, CopyAllPeopleOK, CopyClosingRemarks):
    print("\n------------------------------------------------------------------------------")
    print(f"【学习强国{DateFormat(SelectDay, '%Y年%m月%d日')}学习情况总结】")
    if len(FailList) > 0:
        if len(FailList) > 1:
            print(f"1、{zrSTR}未完成学习的同志共{len(FailList)}位，分别是{FailList}")
        else:
            print(f"1、{zrSTR}未完成学习的同志共{len(FailList)}位，他是{FailList}")
    else:
        print(f"1、{CopyAllPeopleOK}")
    print(f"2、{zrSTR}未上传感想的同志：（迟交1天）")

    if len(Rank2List) > 0:
        if len(Rank2List) > 1:
            print(f"2、特别表扬以下这{len(Rank2List)}位同志，他们分别是{Rank2List}，{CopyBestPeople}")
        else:
            print(f"2、特别表扬{Rank2List}同志，{CopyBestPeople}")
    print(CopyClosingRemarks)

# 输出自己的规则，以便随时取用
def printMyRuleTips(printRuleTips):
    print(printRuleTips)
    print("\n------------------------------------------------------------------------------")

# 最后输出的函数
def printResult(Lists):
    tplt = "{0:^4}\t{1:^4}\t{2:^8}\t{3:^8}\t{4:^8}\t{5:^8}\t{6:<8}"
    print(tplt.format("序号", "姓名", "年度积分", "昨日积分", "当月积分", "总积分", "备注", chr(12288)))
    idx = 1
    for i in Lists:
        print(tplt.format(idx, i[0], i[1], i[2], i[3], i[4], i[5], chr(12288)))
        idx = idx + 1


if __name__ == '__main__':
    try:
        myConfig = readConfigFile(yamlPath)
        myDesktop = myConfig['myDesktop']

        web = getWebObject()
        web.get(XXQG_Login_URL)

        # 格式化日期
        today = date.today()
        DataDate = myConfig['DataDate']
        SelectDay = getDate(DataDate)
        SelectDaySTR = DateFormat(SelectDay, '%Y%m%d')

        # 保存二维码图片去指定位置，监测是否完成扫码，并删除图片
        imgFilesName = saveQRCode()
        WaitClick(ButtonLogin_xpath, "登陆成功!")
        deletePNG(imgFilesName)  # 此时图片没用了，删除即可！
        time.sleep(2)

        # 获取cookies
        cookieDict = {}
        cookieList = web.get_cookies()  # 获取cookies
        for cookie in cookieList:
            cookieDict[cookie['name']] = cookie['value']

        orgGrayId = myConfig['orgGrayId']
        res = sendRequest(cookieDict, orgGrayId, SelectDaySTR, SelectDaySTR)

        OKUseData = json.loads(res['data_str'])['dataList']
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

        CopyBestPeople = myConfig['CopyBestPeople']
        CopyAllPeopleOK = myConfig['CopyAllPeopleOK']
        printRuleTips = myConfig['printRuleTips']
        CopyClosingRemarks = myConfig['CopyClosingRemarks']

        if myConfig['isShowPrintRuleTips']:
            printMyRuleTips(printRuleTips)
        printResult(showList)
        if myConfig['isShowConclusion']:
            printConclusion(CopyBestPeople, CopyAllPeopleOK)
        if myConfig['isShowCopy']:
            printCopy(CopyBestPeople, CopyAllPeopleOK, CopyClosingRemarks)

        web.close()
    except Exception as err:
        print("未知错误：", err)
    finally:
        EscQuit()
