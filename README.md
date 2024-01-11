# 发布视频小程序V2.0
## 介绍
- ~~这是[douyin_uplod](https://github.com/Superheroff/douyin_uplod)的升级版~~
- 比`douyin_uplod`多了**添加话题**、**@人**、**视频抽帧**等功能

## 如何运行
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
│     └── x2.mp4 # 处理后的视频（上传这个视频，上传未处理的会被封号限流）
├── music  # 背景音乐目录
│     └── x.mp3 # 从视频中提取出来的音乐
├── cookie.json  # 登录要发布视频的账号
├── main.py    # 主程序入口
├── config.py  # 配置文件
├── get_cookie.py  # 生成cookie.json文件
├── logs.py  # 生成日志
├── logs.log  # 日志
├── README.md
└── requirements.txt # 依赖文件
```

## 运行逻辑
- 每隔一小时随机从抖音热门音乐下随机选择任意一个作品下载并配上标题发布
- 如有侵权，请联系我删除！
- 联系方式：838210720

# 声明
- qq交流群：916790180
- 本源码只是出于学习交流的目的，使用者造成的任何后果等均与作者无关
