#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
from pymouse import PyMouse, PyMouseEvent
import os
import time
import codecs
from datetime import datetime
from argparse import ArgumentParser
import operator
from terminaltables import AsciiTable
from termcolor import colored

from core.crawler.query import abquery
from core.crawler.baiduzhidao import baidu_count

from core.ocr import get_text_from_image_hanwang, get_text_from_image_baidu

import configparser
import sys

conf = configparser.ConfigParser()
conf.read("config.ini",encoding="utf8")

# ocr_engine = 'baidu'
ocr_engine = conf.get('config',"ocr_engine")

### baidu orc
app_id = conf.get('config',"app_id")
app_key = conf.get('config',"app_key")
app_secret = conf.get('config',"app_secret")

### 0 表示普通识别
### 1 表示精确识别
api_version = conf.get('config',"api_version")

set_plat = conf.get('config',"setplat")
set_area_cd = conf.get('config',"setarea_cd")
set_area_xg = conf.get('config',"setarea_xg")
set_area_bw = conf.get('config',"setarea_bw")
set_area_zs = conf.get('config',"setarea_zs")
# set_area_yzb = conf.get('config',"setarea_yzb")
set_area_uc = conf.get('config',"setarea_uc")
set_area_bd = conf.get('config',"setarea_bd")
set_area_qe = conf.get('config',"setarea_qe")
set_area_cs = conf.get('config',"setarea_cs")
set_area_now = conf.get('config',"setarea_now")

setdely = conf.get('config',"setdely")
# set_area = conf.get('config',"setarea")

### hanwang orc
hanwan_appcode = conf.get('config',"hanwan_appcode")

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = str.upper('#%02x%02x%02x' % rgb_tuple)
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def parse_args():
    parser = ArgumentParser(description="Hiro_QA_Helper")
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="default http request timeout"
    )
    return parser.parse_args()

def extraContext(str,f1,f2):
    left = str.find(f1)
    right = str.rfind(f2)
    return str[left+1:right]

def pre_process_question(qus):
    """
    strip charactor and strip ?
    :param question:
    :return:

    """
    now = datetime.today()
    for char, repl in [("“", ""), ("”", ""), ("？", ""), ("《", ""), ("》", ""), ("我国", "中国"),
                       ("今天", "{0}年{1}月{2}日".format(now.year, now.month, now.day)),
                       ("今年", "{0}年".format(now.year)),
                       ("这个月", "{0}年{1}月".format(now.year, now.month))]:
        qus = qus.replace(char, repl)

    return qus
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_area_data(text_area_file):
    """
    :param text_area_file:
    :return:
    """
    with open(text_area_file, "rb") as fp:
        image_data = fp.read()
        return image_data
    return ""

def main():

    args = parse_args()
    timeout = args.timeout
    start = time.time()
    text_binary = get_area_data("./cut_image.png")

    if ocr_engine == 'baidu':
        # print("百度OCR!!!\n")
        keyword = get_text_from_image_baidu(image_data=text_binary, app_id=app_id, app_key=app_key,
                                            app_secret=app_secret, api_version=api_version, timeout=5)
    else:
        print("汉王 OCR\n")
        keyword = get_text_from_image_hanwang(image_data=text_binary, appcode=hanwan_appcode)

    if not keyword:
        print("Error-1 \n")
        # print("题目出现的时候按F2，我就自动帮你去搜啦~\n")
        return

    question = keyword[0:len(keyword) - 3]
    answers = keyword[len(keyword) - 3:]

    questions = "".join([e.strip("\r\n") for e in question if e])

    # 去掉题目索引
    for char, repl in [("11.", ""), ("12.", ""), ("11、", ""), ("12、", ""), ("1.", ""), ("2.", ""),
                       ("3.", ""), ("4.", ""), ("5.", ""), ("6.", ""), ("7.", ""), ("8.", ""),
                       ("9.", ""), ("10.", ""), ("1、", ""), ("2、", ""), ("3、", ""), ("4、", ""),
                       ("5、", ""), ("6、", ""), ("7、", ""), ("8、", ""), ("9、", ""), ("10、", "")]:
        questions = questions.replace(char, repl)

    print("-" * 70)
    print("问题: | " + questions)
    end3 = time.time()
    print("-" * 50 + "{:4f} 秒".format(end3 - start) + "-" * 10)

    if len(questions) < 2:
        print("没识别出来，随机选吧!!!\n")
        return

    search_question = pre_process_question(questions)

    # ---------------题库关键词输出
    p_ans = []
    for i in range(0, 3):
        for char1, repl1 in [("A.", ""), ("B.", ""), ("C.", ""),
                             ("A、", ""), ("B、", ""), ("C、", ""),
                             ("A：", ""), ("B：", ""), ("C：", ""),
                             ("A:", ""), ("B:", ""), ("C:", "")]:
            answers[i] = answers[i].replace(char1, repl1)

        p_ans.append(answers[i])
    keys = p_ans[:]
    q_key = ""
    if (questions.find("《") != -1) & (questions.rfind("》") != -1):
        q_key = extraContext(questions, "《", "》")
    elif questions.find("\"") != -1:
        pii = questions.find("\"")
        pii1 = questions[pii + 1:].find("\"")
        if pii1 != -1:
            q_key = questions[pii + 1:pii + 1 + pii1]
        else:
            q_key = questions[pii + 1:pii + 5]
    elif questions.find("“") != -1:
        piii = questions.find("“")
        piii1 = questions[piii + 1:].find("”")
        if piii1 != -1:
            q_key = questions[piii + 1:piii + 1 + piii1]
        else:
            q_key = questions[piii + 1:piii + 5]
    elif questions.find("的") != -1:
        q_key = questions[questions.find("的") - 2:questions.find("的") + 2]
    elif questions.find("是") != -1:
        q_key = questions[questions.find("是") - 4:questions.find("是")]
    elif questions.find("哪") != -1:
        q_key = questions[questions.find("哪") - 2:questions.find("哪") + 3]
    elif len(questions) <= 5:
        q_key = questions
    else:
        q_key = questions[6: 10]

    ansl = 0
    if keys:
        fh = codecs.open('dict/dict.txt', "r", "utf-8")
        for line in fh.readlines():
            mao = 0
            if line.find(q_key) != -1:
                for key in keys:
                    if (mao == 0) & (line.find(str(key)) != -1) & (len(str(key)) > 1):
                        if (len(str(key)) < 3) & (is_number(key)):
                            break
                        print(colored(line, "blue"))
                        ansl = 1
                        mao = 1
    if ansl == 0:
        print(colored("《题库》未收录，查询失败!!!!!", "red"))
    else:
        print("问题: | " + questions)
    end2 = time.time()
    print("---------------" + "{:4f} 秒".format(end2 - start) + "----------------")

    # ---------------百度知道API

    summary = baidu_count(search_question, p_ans, timeout=timeout)
    summary_li = sorted(
        summary.items(), key=operator.itemgetter(1), reverse=True)
    data = [("《选项关联度》", "")]
    for a, w in summary_li:
        data.append((a, w))
    table = AsciiTable(data)
    print(table.table)
    end1 = time.time()
    print("---------------" + "{:4f} 秒".format(end1 - start) + "----------------")
    print("---------------百度查询摘要---------------")
    abquery(questions, p_ans, q_key)

    end = time.time()
    print("---------------"+ "{:4f} 秒".format(end - start) + "----------------" )
    time.sleep(20)
    print("Next ING..........")
    dorecycle(setdely)


ans_bg = ""

def dorecycle(setdely):
    while True:
        start = time.time()
        #截取题区
        set_area_list = set_area.split(',')
        # 0,173,255,282
        # 0-173,255,425,286,339,5-389
        os.system("screencapture -R \"0,"+str(set_area_list[0])+","+str(int(set_area_list[1]))+","+str(int(set_area_list[2])-int(set_area_list[0]))+"\" ./cut_image.png")#x1,y1,w1,h1
        question_img = Image.open("./cut_image.png")
        # 校准答案左侧像素
        r1, g1, b1, a1 = question_img.getpixel((3, (int(set_area_list[3])-int(set_area_list[0]))*2))
        r2, g2, b2, a2 = question_img.getpixel((3, (int(set_area_list[4])-int(set_area_list[0]))*2))
        r3, g3, b3, a3 = question_img.getpixel((3, (int(set_area_list[5])-int(set_area_list[0]))*2))
        if ans_bg == "":
            print(colored("请将下行代码粘贴到GetPlatform函数相应位置！！\n"+"ans_bg = \""+RGBToHTMLColor((r1, g1, b1))+"\"","red"))
            time.sleep(25)  # 15秒后重新检测
        else:
            # if (RGBToHTMLColor((r1, g1, b1)) == RGBToHTMLColor((r2, g2, b2))) and (RGBToHTMLColor((r1, g1, b1)) == RGBToHTMLColor((r3, g3, b3))): #观战模式
            if(RGBToHTMLColor((r1, g1, b1)) == ans_bg) and (RGBToHTMLColor((r2, g2, b2)) == ans_bg) and (RGBToHTMLColor((r3, g3, b3)) == ans_bg):
            #     print(RGBToHTMLColor((r1, g1, b1)))
                if setdely == "0":
                    main()
                    break
                else:
                    time.sleep(.5)
                    dorecycle("0")
                    break

cp = 1
ss = []
class ClickListener(PyMouseEvent):


    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        global cp
        global ss
        if button == 1:  # 左键输出位置
            if press:
                if cp <= 5:
                    print("Point"+str(int(cp))+": "+str(int(x))+" "+str(int(y)))
                    print("左键继续")
                    if cp == 1:
                        ss.append(str(int(y)))
                    elif cp == 2:
                        print(str(int(y)))
                        ss.append(str(int(x)))
                        ss.append(str(int(y)))
                    elif cp == 3:
                        print(str(int(y)))
                        ss.append(str(int(y)))
                    elif cp == 4:
                        print(str(int(y)))
                        ss.append(str(int(y)))
                    elif cp == 5:
                        print(str(int(y)))
                        ss.append(str(int(y)))
                else:
                    self.stop()
                    for i in range(1,len(ss)):
                        sss = ",".join(ss)
                    print("请将"+sss+"替换到config.ini文件中 setarea_xx 参数！！！")
                    print("取点关闭！！！")
                cp += 1
        else:# 右键关闭
                self.stop()
                print("关闭取点！！！")


def initArea():
    # 鼠标取5个点（左上，右下，答案1左侧，答案2左侧，答案3左侧）
    clickListener = ClickListener()
    clickListener.run()


def GetPlatform(plat):
    global ans_bg
    if plat == "冲顶大会":
        res = set_area_cd
        ans_bg = "#FEFEFE"
    elif plat == "芝士超人":
        res = set_area_zs
        ans_bg = "#FFFFFF"
    elif plat == "百度视频":
        res = set_area_bd
        ans_bg = "#FFFFFF"
    elif plat == "西瓜视频":
        res = set_area_xg
        ans_bg = "#FFFFFF"
    elif plat == "UC":
        res = set_area_uc
        ans_bg = "#FFFFFF"
    elif plat == "企鹅电竞":
        res = set_area_qe
        ans_bg = "#FFFFFF"
    elif plat == "NOW直播":
        res = set_area_now
        # ans_bg = "#FFFFFF"
        ans_bg = "#EEEFF7"
    # elif plat == "一直播":
    #     res = set_area_yzb
    # elif plat == "一直播":
    #     res = set_area_yzb
    # elif plat == "一直播":
    #     res = set_area_yzb
    else:
        res = ""
    return res

if __name__ == "__main__":
    print('Hiro答题助手启动，请打开config.ini配置setplat以及setarea_xx\n\n' +
              '自动搜索，请注意看题')
    print("---------------当前："+set_plat+"---------------")
    set_area = GetPlatform(set_plat)
    if set_area == "":
        print(colored("请在问题区域(左侧靠近屏幕边缘，覆盖题目与答案区域)取5个点（左上，右下，答案1左侧，答案2左侧，答案3左侧）！！！！\n\n","red"))
        initArea()
    else:
        print('Started')
        print("-" * 70)
        dorecycle(setdely)