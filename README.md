# 发布视频小程序V2.0
## 介绍
- 这是[douyin_uplod](https://github.com/Superheroff/douyin_uplod/tree/main)的升级版
- 比`douyin_uplod`多了**添加话题**、**@人**、**视频抽帧**等功能

## 如何运行
- 使用git clone把项目下载到本地
- 依次运行下面命令，首次使用需要先运行`get_cookie.py`

```shell
pip install -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple/
playwright install chromium
python main.py
```
## 目录结构
```text
douyin_uplod
│
├── frames  # 存放视频抽帧的图片
│     └── x.jpg # 图片
├── video  # 视频目录
│     └── x.mp4 # 未处理的视频
│     └── x2.mp4 # 处理中未添加背景音乐的视频
│     └── x3.mp4 # 处理完的视频（上传的是这个视频，上传未经处理的视频会被限流）
├── music  # 背景音乐目录
│     └── background.mp3 # 从视频中提取出来的音乐
├── cookie.json  # 登录要发布视频的账号
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

# 声明
- qq交流群：916790180
- 有任何问题请到[issues](https://github.com/Superheroff/douyin_uplod/issues)提交
- 本源码只是出于学习交流的目的，使用者造成的任何后果均与作者无关
