# coding:utf-8

# 作者: 明明明明明白了
# 联系我：mmmmmbl@163.com


from selenium.webdriver import Chrome
# 无头浏览器配置需要
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time

# 若chrome升级，请重新升级浏览器驱动
# http://chromedriver.storage.googleapis.com/index.html
# 在该网站查找对应win版本，解压到python解析器文件夹里：D:\develop\Python  -> 这个是自己安装python驱动的位置

# 打包方法： cd .\当前工作目录
# pyinstaller -F .\xxqg-v2.1.py  ⬅这个是要打包的文件夹名字

opt = Options()
# 如果想要页面无法察觉到你是自动的程序，可以这样写，让浏览器的window.navigator=false
opt.add_argument("--disable-blink-features=AutomationControlled")

web = Chrome(options=opt)
url = "https://login.xuexi.cn/login2"
web.get(url)


def WaitClick(xpath, msg=''):
    so = web.find_elements(By.XPATH, xpath)
    while not so:
        time.sleep(1)
        so = web.find_elements(By.XPATH, xpath)
    time.sleep(1)
    so[0].click()
    if msg:
        print(msg)


# 进入按钮
print(f"等待按钮重连。。。")
WaitClick('//*[@id="root"]/div[1]/div/div[2]/form/div/div/div/span/button', "扫码成功!")

# 进入
time.sleep(5)

# 学员
WaitClick('//*[@id="tab-learner"]/span')

# 详细数据
WaitClick('//*[@id="tab-detail"]', "进入主视区域！")
time.sleep(1)

# # 关闭“知道按钮”
# WaitClick('//*[@id="el-popover-2695"]/div[1]/button')
# time.sleep(1)

# 50页版
WaitClick('//*[@id="pane-detail"]/div/div[3]/div/span[2]/div/div/input')
time.sleep(1)
WaitClick('/html/body/div[5]/div[1]/div[1]/ul/li[4]/span', "完成翻页")

# 日期
yesterday = date.today() + timedelta(days=-1)
print(f'昨天日期是：{yesterday}')

td = time.localtime()
if td.tm_mday == 1:
    page = 1
else:
    page = 2
# 获取昨天当月第一天是下星期，若为星期四，y1 = 3
y1 = date(yesterday.year, yesterday.month, 1).weekday()
h = 1
while yesterday.day > h * 7 - y1:
    h = h + 1

WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[1]/div/div')

print(f"点击了第{page} 页\t第{h + 1} 行\t的第{yesterday.weekday() + 1} 个的日期（行包括表头）")
verify_img_element = web.find_element(By.XPATH,
                                      f"/html/body/div[6]/div[1]/div/div[{page}]/table/tbody/tr[{h + 1}]/td[{yesterday.weekday() + 1}]/div/span")
print("即将点击日期是几号：", verify_img_element.text)
time.sleep(1)
ActionChains(web).move_to_element_with_offset(verify_img_element, 20, 15).click().perform()
ActionChains(web).move_to_element_with_offset(verify_img_element, 20, 15).click().perform()
time.sleep(1)
print("完成日期")

# 显示
WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[2]/div/div/span/div/span/div', "完成显示")

# 排序
WaitClick('//*[@id="pane-detail"]/div/div[2]/div[2]/table/thead/tr/th[5]/div/span[3]/i[1]', "完成排序")

# 提交
WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[4]/div/button[1]/span', "即将完成……")

# 抄数据
jk = {
    # 这里是插件生成假数据，不是真人名！
    # 这里是填写自己支部下人员名单和其最低学习的分数……
    "张三": 40, "李四": 40, "黄嘉怡": 40, "史佳琪": 40, "宋榕润": 40,
    "魏文昊": 40, "田佳惠": 40, "王嘉怡": 40, "钱秀英": 40, "贾榕润": 40,
    "龚熙涵": 40, "方溶溶": 40, "蒋益辰": 40, "谢淳美": 40, "吴国贤": 40,
    "雷添昊": 40, "尹甜": 40, "冯尚": 40, "许天昊": 40, "范晨涛": 40, "秦淑慧": 40,
}
no = []
trs = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[2]/div[3]/table/tbody/tr')
print("\t序号", end='\t')
print("姓 名", end='\t')
print("年度积分", end='\t')
print("备注", end='\n')
for mb in trs:
    idname = mb.find_element(By.XPATH, './td[1]/div').text
    print(f"\t{idname}", end='\t')
    name = mb.find_element(By.XPATH, './td[2]/div').text
    if len(name) == 2:
        uname = f"{name[0]}  {name[1]}"
    else:
        uname = name
    print(uname, end='\t')
    njifen = int(mb.find_element(By.XPATH, './td[5]/div').text)
    print(f" {njifen}", end='\t\t')
    if name not in jk:
        print("此党员还不在数据库中，请管理员添加一下吧", end='\n')
    elif njifen < jk[name]:
        print("成绩不合格,请反思", end='\n')
        no.append(name)
    elif njifen >= 50:
        print("【太棒了】", end='\n')
    else:
        print("Good!!!", end='\n')

print(f"\t【{yesterday}日汇总】")
if len(no):
    print(f"\t昨日有{len(no)}位同志未完成学习，分别是{no}")
else:
    print(f"\t昨日所有同志都完成学习，值得鼓励！")
print("\t大家继续加油！")
