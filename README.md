# 发布视频小程序V2.1
## 介绍
- 这是[douyin_uplod](https://github.com/Superheroff/douyin_uplod/tree/main)的升级版
- 比`douyin_uplod`多了**添加话题**、**@人**、**视频抽帧**等功能

## 如何运行
- 使用git clone把项目下载到本地
- 依次运行下面命令，首次使用需要先运行`get_cookie.py`
- 注意：只提供昵称的@并不准确，加抖音号才能完全准确

```shell
pip install -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple/
playwright install chromium
python main.py
```
## 目录结构
```text
douyin_uplod V2
│
├── frames  # 存放视频抽帧的图片
│     └── x.jpg # 图片
├── video  # 视频目录
│     └── x.mp4 # 未处理的视频
│     └── x2.mp4 # 处理中未添加背景音乐的视频
│     └── x3.mp4 # 处理完的视频（上传的是这个视频，上传未经处理的视频会被限流）
├── music  # 背景音乐目录
│     └── background.mp3 # 从视频中提取出来的音乐
├── cookie  # 存放账号目录
│     └── cookie.json # cookie
├── main.py    # 主程序入口
├── config.py  # 配置文件
├── get_cookie.py  # 生成cookie.json文件
├── logs.py  # 生成日志
├── logs.log  # 日志
├── video_id_list.txt  # 记录发过的视频ID，避免重复
├── README.md
└── requirements.txt # 依赖文件
```
## 更新内容
**2024.01.23**
1. 解决`get_cookie`无法获取cookie的问题

**2024.01.17**
1. 修复BUG

**2024.01.15**
1. 解决视频重复问题
2. 新增单双号发布不同的话题内容


**2024.01.12**
1. 优化@人
2. 新增城市定位
3. 新增普通认证号筛选
4. 筛选优化，如全部未有符合条件的内容自动再次获取


**2024.01.11**
1. 优化处理视频
2. 新增筛选：去除图集视频、去除时长过短的视频
3. 优化音乐榜采集，增加随机翻页减少重复视频

## 待优化
- 识别擦边女，拒绝爬取擦边视频


## 运行逻辑
- 每隔1小时随机从抖音热门音乐中选择一首，从选择的音乐中随机提取一条视频，并抽掉前90帧和尾30帧后发布
- 如有侵权，请联系我删除！
- 联系方式：838210720

## 运行日志
```log
视频发布进度: 100%|██████████| 1/1
正在使用[13800138000]发送作品，当前账号排序[1]
正在判断账号是否登录
账号已登录
music_id: 7287937418714892290
url: http://v26-web.douyinvod.com/966d35c0f9f4264ed058cbb5186ef461/65e47ef5/video/tos/cn/tos-cn-ve-15/oQIqDlbAcBeNCg94GHEAKfhAY2zoOgQuANozmC/?a=6383&ch=8&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1574&bt=1574&cs=0&ds=6&ft=bvTKJbQQqUiSf_TZyo0ORVTYA0pinXDrejKJsCAyx.0P3-I&mime_type=video_mp4&qs=0&rc=NjozO2k5PDRkNGk6Mzc6aEBpM2h3aDk6ZnN2cDMzNGkzM0BgNTUwMi80XzMxYDQtMmMyYSNoai0tcjRnbC5gLS1kLS9zcw%3D%3D&btag=e00028000&cquery=100a&dy_q=1709469854&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=20240303204414067063A99F18A94D4196
nickname: 小猛猛
video_id: 7314915554131774758
处理前md5： 99c8f86699f0050856706bdb126d1449
正在处理视频
视频抽帧进度: 100%|██████████| 2012/2012 [00:29<00:00, 69.36it/s]
图片合成进度: 100%|█████████▉| 2011/2012 [00:09<00:00, 207.02it/s]
开始添加背景音乐！
MoviePy - Writing audio in music/background.mp3
MoviePy - Done.
Moviepy - Building video E:\python\douyin\发布小程序\video\3.mp4.
MoviePy - Writing audio in .mp3
t:   0%|          | 0/2011 [00:00<?, ?it/s, now=None]MoviePy - Done.
Moviepy - Writing video E:\python\douyin\发布小程序\video\3.mp4

Moviepy - Done !
Moviepy - video ready E:\python\douyin\发布小程序\video\3.mp4
背景音乐添加完成！
[2024-03-03 20:45:33,868]-main.py-450-MainThread-视频下载成功，等待发布
处理后md5： b44c717b2e288b44dc93549b00e5c589
视频处理完毕
该视频有话题
Timeout 30000ms exceeded.
正在添加第1个话题
正在添加第2个话题
正在添加第3个话题
正在添加第4个话题
正在添加第5个话题
正在添加第1个想@的人
[2024-03-03 20:46:13,045]-main.py-505-MainThread-@xxx失败了，可能被对方拉黑了
@xxx失败了，可能被对方拉黑了
正在添加第6个话题
正在添加第2个想@的人
想@的人 小猛猛
正在添加第7个话题
视频标题输入完毕，等待发布
位置添加成功
视频发布成功
```

# 声明
- qq交流群：916790180
- 有任何问题请到[issues](https://github.com/Superheroff/douyin_uplod/issues)提交
- 本源码只是出于学习交流的目的，使用者造成的任何后果均与作者无关
