# -*- coding: utf8 -*-
import json
import time
import requests
import re
from enum import Enum

# 是否开启通知
openPush = True
# PUSH PLUS 通知Token
PUSH_TOKEN = ''
PUSH_NOTITY_DATA = []  # 通知数据集合

# Bing ck 集合，多个ck请按列表形式输入
CKList = [
“BIDUPSID=B7E16FAEC33EF6A7C679AD96C32D08B2; PSTM=1650014457; newlogin=1; BDUSS=nJpQVNFTnp6dFYtTHREb0xNbUJUUVE0UFVqRzlNVUJBemRJeGZsRjktVE1EVkprRVFBQUFBJCQAAAAAAAAAAAEAAAA-mWbCaGVsbG9DYUJCQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMyAKmTMgCpkN; BDUSS_BFESS=nJpQVNFTnp6dFYtTHREb0xNbUJUUVE0UFVqRzlNVUJBemRJeGZsRjktVE1EVkprRVFBQUFBJCQAAAAAAAAAAAEAAAA-mWbCaGVsbG9DYUJCQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMyAKmTMgCpkN; BAIDUID=DE864F47864661774330AD1E801EBA9A:FG=1; BD_UPN=12314753; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; MCITY=-134%3A; H_PS_PSSID=26350; BAIDUID_BFESS=DE864F47864661774330AD1E801EBA9A:FG=1; BA_HECTOR=a50ga08021ah8001agakak8g1ia7d7t1o; ZFY=Auvt8q1j:B098Wo1CSisr8Edz3arwKwft1Lq12rU4iLU:C; BDRCVFR[ygjMp2nIKjY]=mk3SLVN4HKm; delPer=0; BD_CK_SAM=1; PSINO=7; H_PS_645EC=9da1yRjLjuL8qUx2H0yxN0TvqPOnZmtJSbyijzrw3rgAmBcewOFyOAy%2BnOoQfwwWDeDtnw; baikeVisitId=50e4da63-31c5-4316-9fa0-fe14a21e5cff”
]


class BrowserUA(Enum):
    PC = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64'
    MOBILE = 'Mozilla/5.0 (Linux; Android 13; 22041211AC Build/TP1A.220624.014; ) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 BingSapphire/23.8.2110003536'


class Bing:
    def __init__(self, cookie):
        self.cookie = cookie
        self.more_promotions = None
        self.csrf_token = None
        self.username = None
        self.level = None
        self.point = None
        self.today_point = None
        self.ua = BrowserUA.PC.value
        self.headers = {
            'cookie': self.cookie,
            'user-agent': self.ua,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def init_data(self):
        self.ua = BrowserUA.PC.value
        url = "https://rewards.bing.com/"
        try:
            result = requests.get(url, headers=self.headers).text
            print(result)
            dash_board = re.findall(r'var dashboard = {(.*?)};', result, flags=0)[0]
            dash_board = f'{{{dash_board}}}'

            self.username = re.findall(r'class="mectrl_truncate">(.*?)</div>', result)[0]
            self.csrf_token = \
                re.findall(r'<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />', result, flags=0)[
                    0]
            dash_board_json = json.loads(dash_board)
            self.more_promotions = dash_board_json['morePromotions']
            self.level = int(dash_board_json['userStatus']['levelInfo']['activeLevel'][5:])
            self.point = dash_board_json['userStatus']['availablePoints']
            self.today_point = dash_board_json['userStatus']['counters']['dailyPoint'][0]['pointProgress']
            return True
        except:
            print("请检查CK是否正确或者是否已过期")
            return False

    def bing_search(self, keyword):
        url = f"https://cn.bing.com/search?q={keyword}"
        requests.get(url, headers=self.headers)

    def report_activity(self, id, hash, token):
        self.ua = BrowserUA.PC.value
        url = 'https://rewards.bing.com/api/reportactivity?X-Requested-With=XMLHttpRequest'
        data = f'id={id}&hash={hash}&timeZone=480&activityAmount=1&__RequestVerificationToken={token}'
        result = requests.post(url, data=data, headers=self.headers)
        print(result.text)

    def do_daily_activities(self):
        for i in range(len(self.more_promotions)):
            activity_str = json.dumps(self.more_promotions[i])
            activity = json.loads(activity_str)
            id = activity['offerId']
            hash = activity['hash']
            complete = activity['complete']
            if complete != True:
                self.report_activity(id, hash, self.csrf_token)
                time.sleep(0.1)

    def do_daily_search(self):
        if (self.level == 1):
            self.ua = BrowserUA.PC.value
            keywords = ['java', 'Java', 'JAVA', 'python', 'Python', 'jvm', 'Jvm', 'JVM', 'spring', 'Spring', 'bing',
                        'Bing',
                        'BING']
            for i in range(len(keywords)):
                self.bing_search(keywords[i])
                # print(f"必应搜索[{keywords[i]}]完成")
                time.sleep(0.1)
        elif (self.level == 2):
            self.ua = BrowserUA.PC.value
            keywords = ['bing', 'Bing', 'BING', '必应', '小米', 'MI', 'xiaomi', '华为', 'huawei', '苹果', 'apple', 'Oppo', '一加',
                        'OnePlus', 'oneplus', '真我',
                        'RealMe', '红米', 'RedMi', 'Vivo', 'Iqoo', '魅族', 'Flyme', '三星', '谷歌', 'Google', '淘宝', '天猫', '京东',
                        '拼多多', '长安', '吉利',
                        '混沌', '太极', '两仪', '三才', '四象', '五行', '六合', '七星', '八卦', '九宫']
            for i in range(len(keywords)):
                self.bing_search(keywords[i])
                # print(f"必应搜索[{keywords[i]}]完成")
                time.sleep(0.1)
            self.ua = BrowserUA.MOBILE.value
            keywords = ['java', 'Java', 'JAVA', 'python', 'Python', 'jvm', 'Jvm', 'JVM', 'spring', 'Spring', 'bing',
                        'Bing',
                        'BING', '必应', '小米', 'MI', 'xiaomi', '华为', 'huawei', '苹果', 'apple']
            for i in range(len(keywords)):
                self.bing_search(keywords[i])
                # print(f"必应搜索[{keywords[i]}]完成")
                time.sleep(0.1)

    def do_task(self):

        if not self.init_data(): return
        print(f'你的等级：{self.level}，总积分：{self.point}，今日积分：{self.today_point}')
        print("-" * 25)
        print("开始执行任务，请耐心等待完成")
        self.do_daily_activities()
        self.do_daily_search()
        print("-" * 25)
        print("今日任务已完成")

        self.init_data()
        push_data = f'| {self.username} '
        push_data = push_data + f'| Lv.{self.level}'
        push_data = push_data + f'| {self.point}'
        push_data = push_data + f'| {self.today_point}  |'
        PUSH_NOTITY_DATA.append(push_data)
        print(f'你的等级：{self.level}，总积分：{self.point}，今日积分：{self.today_point}')


# markdown代码，请勿更改
PUSH_BASE_DATA = '''<style>
  table {
      width: 100%; /*表格宽度*/
      border-collapse: collapse; /*使用单一线条的边框*/
      empty-cells: show; /*单元格无内容依旧绘制边框*/
  }

  table th {
      font-weight: bold; /*加粗*/
      text-align: center !important; /*内容居中，加上 !important 避免被 Markdown 样式覆盖*/
      background: #ECFBF2; /*背景色*/
      white-space: nowrap; /*表头内容强制在一行显示*/
      color: #43D384;
  }

  table td{
      white-space: nowrap; 
      text-align: center !important;
  }
  </style>  

微软今日任务完成啦
-----------------
| 登录账户 | 任务等级 | 可用积分 | 今日积分 |
|:----------|:-----:|:-----:|:-----:|'''


def sendPush(title, body):
    content = f'{body}  \n***  \n'
    content = content + f'__[执行时间]：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}__  \n'
    content = content + '__[来源渠道]：微软任务签到脚本 by 逍遥&沫湮__  \n'
    print(content)
    data = {
        'token': PUSH_TOKEN,
        'title': title,
        'content': content,
        'template': 'markdown'
    }
    url = 'http://www.pushplus.plus/send'
    res = requests.post(url, json=data).text
    print(res)


# 腾讯云主函数入口
def main_handler(event, context):
    for cookie in CKList:
        bing = Bing(cookie)
        bing.do_task()

    if openPush and PUSH_TOKEN and len(PUSH_TOKEN) > 0 and len(PUSH_NOTITY_DATA) > 0:
        push_data = PUSH_BASE_DATA + '\n'
        for s in PUSH_NOTITY_DATA:
            push_data += s + '\n'
        sendPush('微软定时任务完成！', push_data)
    return None


if __name__ == '__main__':
    main_handler(None, None)
