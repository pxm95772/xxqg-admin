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

opt = Options()
# 如果想要页面无法察觉到你是自动的程序，可以这样写，让浏览器的window.navigator=false
opt.add_argument("--disable-blink-features=AutomationControlled")

web = Chrome(options=opt)
url = "https://login.xuexi.cn/login2"
web.get(url)

# 进入按钮
so = web.find_elements(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/form/div/div/div/span/button')
while not so:
    print(f"按钮重连。。。")
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/form/div/div/div/span/button')
print("扫码成功!")
# 进入
so[0].click()

time.sleep(5)

# 学员
so = web.find_elements(By.XPATH, '//*[@id="tab-learner"]/span')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="tab-learner"]/span')
time.sleep(1)
so[0].click()

# 详细数据
so = web.find_elements(By.XPATH, '//*[@id="tab-detail"]')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="tab-detail"]')
time.sleep(1)
so[0].click()
print("进入主视区域！")
time.sleep(1)

# 30页版
so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[3]/div/span[2]/div/div/input')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[3]/div/span[2]/div/div/input')
so[0].click()
time.sleep(1)

soo = web.find_elements(By.XPATH, '/html/body/div[5]/div[1]/div[1]/ul/li[4]/span')
while not soo:
    time.sleep(1)
    soo = web.find_elements(By.XPATH, '/html/body/div[5]/div[1]/div[1]/ul/li[4]/span')
soo[0].click()

print("完成翻页")

# 日期
yesterday = date.today() + timedelta(days=-1)
print(f'昨天日期是：{yesterday}')

td = time.localtime()
if td.tm_mday == 1:
    page = 1
else:
    page = 2

y1 = date(yesterday.year, yesterday.month, 1).weekday()
h = 1
while yesterday.day > h * 7 - y1:
    h = h + 1

so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[1]/div/div')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[1]/div/div')
so[0].click()

print(f"page:{page}\th:{h + 1}\tr:{yesterday.weekday() + 1}")
verify_img_element = web.find_element(By.XPATH,
                                      f"/html/body/div[6]/div[1]/div/div[{page}]/table/tbody/tr[{h + 1}]/td[{yesterday.weekday() + 1}]/div/span")
time.sleep(1)
ActionChains(web).move_to_element_with_offset(verify_img_element, 20, 15).click().perform()
ActionChains(web).move_to_element_with_offset(verify_img_element, 20, 15).click().perform()
print("完成日期")

# 显示
time.sleep(1)
so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[2]/div/div/span/div/span/div')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[2]/div/div/span/div/span/div')
so[0].click()
print("完成显示")

# 排序
so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[2]/div[2]/table/thead/tr/th[5]/div/span[3]/i[1]')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[2]/div[2]/table/thead/tr/th[5]/div/span[3]/i[1]')
so[0].click()
print("完成排序")

# 提交
so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[4]/div/button[1]/span')
while not so:
    time.sleep(1)
    so = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[4]/div/button[1]/span')
so[0].click()
print("即将完成。。。。。", end='\n')

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
    uname = mb.find_element(By.XPATH, './td[2]/div').text
    if len(uname) == 2:
        una = f"{uname[0]}  {uname[1]}"
    else:
        una = uname
    print(una, end='\t')
    njifen = mb.find_element(By.XPATH, './td[5]/div').text
    print(f" {njifen}", end='\t\t')
    if int(njifen) < jk[uname]:
        print("成绩不合格,请反思", end='\n')
        no.append(uname)
    elif int(njifen) >= 50:
        print("【太棒了】", end='\n')
    else:
        print("Good!!!", end='\n')

print(f"\t【{yesterday}日汇总】")
print(f"\t昨日有{len(no)}位同志未完成学习，分别是{no}")
print("\t大家继续加油！")
