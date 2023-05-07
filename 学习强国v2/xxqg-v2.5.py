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
# pyinstaller -F .\xxqg-v2.5.py  ⬅这个是要打包的文件夹名

# v3.4版本解决了：
#       1、更新名单
#       2、关闭进程

# PS：页面的xpath很恶心，对应的控制条数、日期选项卡都是点后插入，所以在寻找对应xpath时就要考虑对应元素是否进入了
# 如 "/html/body/div[6]/div[1]/div/div[2]/div/div" 里的 6 就是需要先有日期的框进入，在进入的框就是6，下一个框时7，以此类推

opt = Options()
# 如果想要页面无法察觉到你是自动的程序，可以这样写，让浏览器的window.navigator=false
opt.add_argument("--disable-blink-features=AutomationControlled")

web = Chrome(options=opt)
url = "https://login.xuexi.cn/login2"
web.get(url)

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

def selectDay(today):
    # 寻找参数当天在日期选择里的位置函数（找昨天就传昨天的日期）
    # 返回参数对应日期对象的xpath
    tomorrow = today + timedelta(days=+1)
    print(f'今天是：{today}，明天是：{tomorrow}，这里的今天是相对于传入参数的今天')

    # 获取对应页数
    if tomorrow.day == 1 or tomorrow.day == 31:
        page = 1
    else:
        page = 2
    msg = web.find_element(By.XPATH, f"/html/body/div[6]/div[1]/div/div[{page}]/div/div").text.strip()
    # 获取昨天当月第一天是下星期，若为星期四，y1 = 3
    y1 = date(today.year, today.month, 1).weekday()
    h = 1
    while today.day > h * 7 - y1:
        h = h + 1

    el = web.find_element(By.XPATH, f"/html/body/div[6]/div[1]/div/div[{page}]/table/tbody/tr[{h + 1}]/td[{yesterday.weekday() + 1}]/div/span")
    # 控制台确认信息
    print(f"对象选中了日期是 {msg} {el.text.strip()} 号！")
    print(f"即将点击了第 {page} 页第 {h + 1} 行的第 {today.weekday() + 1} 个的日期（行包括表头）")
    return el

def memorandum():
    # 备忘录函数
    print("-------【备用模板】--------------------")
    print("2、各位同志在写检讨书时，请端正态度、端正字迹！结尾不能缺少落款时间，且不能涂改。")
    print("2、还未修改备注的同志请按“班级+姓名+身份+电话”，如“计科201张三1829******51”修改群备注")
    print("2、在积分页面右上角有个积分细则，蓝色括号内的年度积分才算数，不是看当日积分！")
    print("如还有疑问可以直接在群里问，或单独联系我。")
    print("2、未上传检讨：")
    print("""【关于“学习强国”学习小组每日常规】
        1、每天学习强国的“计入年度积分”不低于40分，且每位同志请在晚上11点前完成当天的学习，不用交截图！
        2、新一批进入学习强国小组的同志的要求是前两个月尽可能把每天的积分全部刷满，因为需要把本年度前面的每周答题和专项答题尽快补完。（至少肯定是有50）。
        3、对于每天未完成学习的同志，管理员会在本群@，请该同志积极反思、学习，并写一篇感想。
        4、感想公式：在首页自行找近期通报当天2天内的文章或视频，进行写感想。点击文章右上方三点，复制链接，链接很长，只需要摘抄链接问号后的第一个参数即可，如：https://article.xuexi.cn/articles/index.html?art_id=2978574176247223543。
        5、感想提交要求：至少一页信纸，字迹工整、注意检讨格式。每次提交上传到这个群文件夹即可图片即可，不用插入pdf或word.文件重命名:学习强国学习感想＋日期+姓名如:学习强国感想+2022/10/01+张三.jpg不重命名或未放入指定群文件夹，会@重交哦!（必须要有落款姓名和时间，不得涂改）【字数不够、字迹潦草、重复提交等态度不端正行为情况都需要重新写检查】。要求当天@，当天就要写完并拍照发在本群中；若第二天还未完成上传，管理员会再次提醒；多次提醒未有效果，名单将交由支部书记。
        6、请全体同志重新修改本群群昵称为班级+姓名+身份+电话，如：计科201张三1829******51。
        【特殊情况】：对于校外的同志写感想上传时间可以适当延长，可以不是学校的信纸，但也必须用信纸。信纸在如何地方周边文具店购买，上传时间不得超过3天。有其他特殊情况需一定要向管理员和老师及时说明情况。""")
    print("---------------------------")


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
WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[1]/div/div')
time.sleep(1)

# 获取今天和昨天日期
today = date.today()
yesterday = today + timedelta(days=-1)
# 调用函数获取昨天的点击对象
today_element = selectDay(yesterday)
time.sleep(1)

ActionChains(web).move_to_element_with_offset(today_element, 20, 15).click().perform()
ActionChains(web).move_to_element_with_offset(today_element, 20, 15).click().perform()
time.sleep(1)
print("完成日期")

# 显示
WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[2]/div/div/span/div/span/div', "完成显示")

# 排序
WaitClick('//*[@id="pane-detail"]/div/div[2]/div[2]/table/thead/tr/th[5]/div/span[3]/i[1]', "完成排序")

# 提交
WaitClick('//*[@id="pane-detail"]/div/div[1]/div/div[1]/form/div[4]/div/button[1]/span', "即将完成……")

# 书写备忘
memorandum()

# 抄数据
# 预备党员、党员在jk（计科）中，其他要求的成员放fzdx中
FenJK = 40
FenFZDX = 50
jk = [
    # 这里是插件生成假数据，不是真人名！
    "卢强", "沈嘉怡", "毛雅涵", "董欣汝", "魏欣欣",
    "范佳惠", "余淑慧", "董淑华", "许嘉怡", "杨淑君",
    "冯欣源", "高杨", "曹欣慧", "朱淼", "毛佳琪",
    "万欣欣", "雷清妍", "曾瑞辰", "谭清妍", "梁冰洁"
],
fzdx  = [

]

# 未完成、特别表扬临时数组
no = []
good = []

trs = web.find_elements(By.XPATH, '//*[@id="pane-detail"]/div/div[2]/div[3]/table/tbody/tr')
print("\t序号", end='\t')
print("姓 名", end='\t')
print("年度积分", end='\t')
print("备注", end='\n')
for mb in trs:
    # 用户序号（排名）
    xuhao = mb.find_element(By.XPATH, './td[1]/div').text
    print(f"\t{xuhao}", end='\t')

    # 用户姓名
    name = mb.find_element(By.XPATH, './td[2]/div').text
    if len(name) == 2:
        uname = f"{name[0]}  {name[1]}"
    else:
        uname = name
    print(uname, end='\t')

    # 获取用户年度积分
    njifen = int(mb.find_element(By.XPATH, './td[5]/div').text)
    print(f" {njifen}", end='\t\t')

    # 判断用户身份：
    if name in jk:
        if njifen < FenJK:
            print("成绩不合格,请反思！", end='\n')
            no.append(name)
        elif njifen >= FenJK + 10:
            print("★太强了！你一定认真学习了很久吧！", end='\n')
            good.append(name)
        elif njifen >= FenJK + 5:
            print("太棒了！Good!!!", end='\n')
        elif njifen == FenJK:
            print("不要总是40分哦！嘿嘿", end='\n')
        else:
            print("合格", end='\n')
    elif name in fzdx:
        if njifen < FenFZDX:
            print(f"成绩低于{FenFZDX}分,请检讨反思！", end='\n')
            no.append(name)
        elif njifen >= FenFZDX + 6:
            print("★太强了！你一定认真学习了很久吧！", end='\n')
            good.append(name)
        else:
            print("合格", end='\n')
    else:
        print("此党员还不在数据库中，请管理员添加一下吧", end='\n')


print(f"\t学习强国【{yesterday}日汇总】")
if len(no):
    print(f"\t昨日共有 {len(no)} 位同志未完成学习，分别是{no}")
else:
    print(f"\t昨日所有同志都完成学习，值得鼓励！")
print(f"\t今天特别表扬以下这{len(good)}位同志，分别是{good}")
print("\t学而时习之，不亦说乎！~~~大家继续加油！", end='\n\n')

print("-------【输出模板】--------------------", end='\n')
print(f"【学习强国{yesterday.month}月{yesterday.day}日学习情况】")
if len(no) > 0:
    print("1、未完成学习的同志：")
else:
    print("1、已连续<???>天清0，最大连续10天。")
print("-------------------------------------", end='\n\n')

web.close()



