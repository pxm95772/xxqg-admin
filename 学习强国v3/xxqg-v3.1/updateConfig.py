# coding:utf-8

# 安装yaml，在终端输入：npm install yaml
import yaml

# config文件的地址
yamlPath = "./config.yaml"

# 会存在config配置里的数据
updatedData = {
    # 请根据自身电脑桌面位置填写（推荐放桌面主要是方便快速找到生成的截图，其实放别的文件夹也是可以的）（必填★★★★★）
    "myDesktop": "C://桌面",
    # 想要哪天的数据：0是今天，-1是昨天，-2是前天，以此类推；若填日期则是查看对应日期的数据（暂不支持）
    "DataDate": -1,
    # 组织ID，可以自行获取，在network中获取，不填应该也没事
    "orgGrayId": "",
    # 在下面各个学习组里未找到该同志的备注信息
    "NotFindTips": "该同志还不在系统中，请联系管理员添加信息",
    # 每当所有同志都完成了学习时会输出的话。
    "CopyAllPeopleOK": "昨日所有同志都完成的了学习！请大家继续保持。",
    # 当有同志分数达到rank2时，会输出的话
    "CopyBestPeople": "请其他同志向他们学习！",
    "isShowCopy": True,
    "isShowConclusion": True,
    # 在可复制段落的最后一句话
    "CopyClosingRemarks": "学而时习之，不亦说乎！~~~大家继续加油！",

    # 学习群组（每个组可以设置人员列表和规则列表）
    # 可以添加多个学习组，每组必须要有People和Rules对象，用于存人员名字数组和规则数组。
    # 规则数组里，每一条是一个对象，name是规则等级名，rank是指低于这个分数（不包括这个分数）则就是这个等级，Tips是该等级会返回的备注。
    # 【重要】若想要收集不合格、不错、非常好部分同志，规则名必须分别是Fail、Rank1、Rank2，否则暂时不收集
    "StudyGroup": {
        "JKDY": {
            "People": [
                "张三", "张三", "张三", "张三", "张三",
            ],
            "Rules": [
                {"name": "Fail", "rank": 40, "Tips": "低于40分"},
                {"name": "Warn", "rank": 41, "Tips": "低于41分"},
                {"name": "Default", "rank": 45, "Tips": "低于45分"},
                {"name": "Rank1", "rank": 50, "Tips": "低于50分"},
                {"name": "Rank2", "rank": 100, "Tips": "大于等于50分"},
            ]
        },
        "JKFZDX": {
            "People": [
                "测试人员",
            ],
            "Rules": [
                {"name": "Fail", "rank": 45, "Tips": "不合格"},
                {"name": "Default", "rank": 49, "Tips": "合格"},
                {"name": "Rank1", "rank": 53, "Tips": "Good！"},
                {"name": "Rank2", "rank": 100, "Tips": "太强了"},
            ],
        }
    },

    # 设置默认输出的模板，推荐顶格写，便于输出后复制。
    "isShowPrintRuleTips": True,
    "printRuleTips": """
-------【备用模板】--------------------"
可以在这里留存你的备用模板，比如经常可能会到的话，便于来复制。
推荐定格写，这样输出时也是相对于命令行定格的，利于查看、复制等等。。。。
你也可以在这里使用\n来换行输入！
    """,

}

with open(yamlPath, 'w', encoding='utf-8') as f:
    yaml.dump(data=updatedData, stream=f, allow_unicode=True)
