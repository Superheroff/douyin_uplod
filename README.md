# 发布视频小程序V2.3
## 介绍
- [old_douyin_uplod](https://github.com/Superheroff/douyin_uplod/tree/main)
- 比`old_douyin_uplod`多了**添加话题**、**@人**、**视频抽帧**等功能

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
│     └── cookie_手机号.json # cookie
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
**2024.03.07**
1. 新增视频声明配置
2. 新增视频定位开关配置
3. 解决了一些问题

**2024.03.04**
1. 修复文件路径问题
2. 新增视频发布进度条
3. 新增视频声明
4. 先判断是否登录再处理视频，解决先处理视频后发现未登录的尴尬场景

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
正在使用[15579611112]发布作品，当前账号排序[1]
正在判断账号是否登录
账号已登录
music_id: 7312850623345527603
url: http://v3-web.douyinvod.com/e5be13cd66c2e99df4a5dc8d74a4bff4/65e4afcf/video/tos/cn/tos-cn-ve-15/ocwAH9yEbELzxBwIgKCLYthCfAAe3Q7Dyr9TGI/?a=6383&ch=8&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1289&bt=1289&cs=0&ds=4&ft=bvTKJbQQqUiSf_TZyo0ORVTYA0pijkIrejKJsCAyx.0P3-I&mime_type=video_mp4&qs=0&rc=ZjU1OjU8ZjhlNzU7ZDs8NUBpamU2azY6ZjhrcTMzNGkzM0A2NC80Y18yXjYxLTNgYWFhYSNpbjM2cjRfcWFgLS1kLS9zcw%3D%3D&btag=e00018000&cquery=100a&dy_q=1709482393&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=20240304001313B4854C73E6800D57BF70
nickname: 黏苞米糊糊
video_id: 7339494544162983204
处理前md5： 4453555b2ac6c4b6c9d844d94d27301d
正在处理视频
视频抽帧进度: 100%|██████████| 1047/1047 [00:39<00:00, 26.44it/s]
图片合成进度: 100%|█████████▉| 1046/1047 [00:14<00:00, 72.67it/s]
开始添加背景音乐！
MoviePy - Writing audio in music/background.mp3
MoviePy - Done.
Moviepy - Building video E:\python\douyin\发布小程序\video\#标题2 @1486323920 —来自：音乐榜单的第2个音乐《身骑白马 (pay姐版) 已全网上线》第13页第5个@黏苞米糊糊 的作品3.mp4.
MoviePy - Writing audio in #标题2 @1486323920 —来自：音乐榜单的第2个音乐《身骑白马 (pay姐版) 已全网上线》第13页第5个@黏苞米糊糊 的作品3TEMP_MPY_wvf_snd.mp3
t:   0%|          | 0/1047 [00:00<?, ?it/s, now=None]MoviePy - Done.
Moviepy - Writing video E:\python\douyin\发布小程序\video\#标题2 @1486323920 —来自：音乐榜单的第2个音乐《身骑白马 (pay姐版) 已全网上线》第13页第5个@黏苞米糊糊 的作品3.mp4

t: 100%|█████████▉| 1046/1047 [00:25<00:00, 43.60it/s, now=None][2024-03-04 00:14:57,566]-warnings.py-109-MainThread-E:\python\douyin\发布小程序\venv\Lib\site-packages\moviepy\video\io\ffmpeg_reader.py:123: UserWarning: Warning: in file E:\python\douyin\发布小程序\video\#标题2 @1486323920 —来自：音乐榜单的第2个音乐《身骑白马 (pay姐版) 已全网上线》第13页第5个@黏苞米糊糊 的作品2.mp4, 6220800 bytes wanted but 0 bytes read,at frame 1046/1047, at time 34.87/34.87 sec. Using the last valid frame instead.
  warnings.warn("Warning: in file %s, "%(self.filename)+

Moviepy - Done !
Moviepy - video ready E:\python\douyin\发布小程序\video\#标题2 @1486323920 —来自：音乐榜单的第2个音乐《身骑白马 (pay姐版) 已全网上线》第13页第5个@黏苞米糊糊 的作品3.mp4
背景音乐添加完成！
处理后md5： f97a9c8b2140a228142db443937f6b79
视频处理完毕
该视频有话题
[2024-03-04 00:14:59,035]-main.py-450-MainThread-视频下载成功，等待发布
Timeout 30000ms exceeded.
正在添加第1个话题
正在添加第1个想@的人
[2024-03-04 00:15:37,533]-main.py-505-MainThread-@1486323920失败了，可能被对方拉黑了
@1486323920失败了，可能被对方拉黑了
正在添加第2个话题
正在添加第3个话题
正在添加第2个想@的人
想@的人 黏苞米糊糊
正在添加第4个话题
视频标题输入完毕，等待发布
位置添加成功
[2024-03-04 00:15:51,116]-main.py-538-MainThread-账号发布视频成功
[2024-03-04 00:15:51,205]-main.py-549-MainThread-账号发布视频成功
来自网页的实时消息：发布成功
账号发布视频成功
```

# 声明
- qq交流群：916790180
- 有任何问题请到[issues](https://github.com/Superheroff/douyin_uplod/issues)提交
- 本源码只是出于学习交流的目的，使用者造成的任何后果均与作者无关
