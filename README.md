## Hiro直播答题助手——for MAC

## 自动检测出题，自动搜索答案

## 支持（冲顶大会、优酷视频、知识超人等平台）

## 视频演示

[mow1.mp4](/figure/mow1.mp4)

#### Quiketime Player （QP）+ iphone

## 实现

1. Quiketime Player 获取屏幕显示
2. 截取题区
3. 百度ORC识图（返回问题与选项）

## 自动检测

自动检测出题逻辑很简单，获取三个选项框某一点的位置，获取颜色，判断相同即将题区截图发送ORC识别文字并搜索

## 效果演示

![pig1](/figure/pig1.jpg)

共三个部分

1. 题库输出（根据问题关键词或答案查询题库）

2. 百度知道API输出（个人经验，只对部分提醒正确率较高，对于否定选择以及逻辑判断题无效）

3. 百度搜索摘要（完整句子中的信息才是有效信息）此处进行一下搜索

   > Search question
   >
   > if null search question + "key(for key in keys)"

题库输出演示

![pig2](/figure/pig2.jpg)

#### 注意：彩色字体输出使用的termcolor库，目前测试只在Pycharm中能显示颜色字体

## 编译：

- python3.6 
- Pycharm IDE

## 配置：

- QP打开桌面缩小到最小窗口放置到屏幕左侧
- 编译通过后，打开对应平台截图一张

![fig4](/figure/fig4.png)

- 将QP窗口左移，使得题区左侧信息隐藏

  > 为了给右侧更大的屏幕空间


- 运行main.py

## 代码部分

#### 打开config.ini设置平台

```
setplat =测试
# 芝士超人 百度视频 冲顶大会 西瓜视频 UC 企鹅电竞
```

#### setarea_xx参数为对应

![fig5](/figure/fig5.png)

```
Hiro答题助手启动，请打开config.ini配置setplat setarea_xx

自动搜索，请注意看题
---------------当前：测试---------------
请在问题区域(左侧靠近屏幕边缘，覆盖题目与答案区域)取5个点（左上，右下，答案1左侧，答案2左侧，答案3左侧）！！！！


Point1: 1 145
左键继续
Point2: 282 421
左键继续
421
Point3: 3 252
左键继续
252
Point4: 4 323
左键继续
323
Point5: 5 394
左键继续
394
请将145,282,421,252,323,394替换到config.ini文件中 setarea_xx 参数！！！
取点关闭！！！
```

#### 将145, 。。。,394替换到config.ini文件中 setarea_xx 参数

```
#测试
setarea_cs =145,282,421,252,323,394
#冲顶大会
setarea_cd =136,270,418,285,337,391
#西瓜视频
setarea_xg =106,281,388,256,314,367
```

#### 再次运行，输出以下信息

```
请将下行代码粘贴到GetPlatform函数相应位置！！
ans_bg = "#F2F2F2"
```

#### 关闭程序，找到GetPlatform()在相应位置添加“ans_bg = "#F2F2F2"”

```
...
elif plat == "测试":
    res = set_area_cs
    ans_bg = "#F2F2F2"
...
```

#### 再次运行

