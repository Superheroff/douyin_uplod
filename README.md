# 发布视频小程序V2.0
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
music_id: 7215811630108510210
该视频:7285622795827006783已经发送过了本次不再发送
该视频:7285622795827006783已经发送过了本次不再发送
url: http://v26-web.douyinvod.com/15f197ff8bdde0766f6b1b8ebb89c0a3/65a781f9/video/tos/cn/tos-cn-ve-15/oQ3U7LMeCoXHBKffBARJIhI2oHoAd5gPBrGCog/?a=6383&ch=8&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=4801&bt=4801&cs=0&ds=4&ft=bvTKJbQQqUYqfJEZao0OiJTidUpi-UM_ejKJz-fVoG0P3-I&mime_type=video_mp4&qs=0&rc=aDlpODw4NGg0aTo5Ozc6OkBpM2w6c2Y6ZjhqcDMzNGkzM0BgX18xYDNeXjUxLzNhYTJiYSMyaWI0cjQwLy9gLS1kLTBzcw%3D%3D&btag=e00018000&dy_q=1705472969&feature_id=46a7bb47b4fd1280f3d3825bf2b29388&l=20240117142928CAC1860DB4F6D57378BA
nickname: 宸宸不挑食
video_id: 7315254519003204914
处理前md5： ec1ecb9360625d8e45469cf18a821171
正在处理视频
已处理 90/944 帧
......
已处理 944/944 帧
所有帧都已成功抽取！
第1张图片合成成功
......
第854张图片合成成功
开始添加背景音乐！
MoviePy - Writing audio in music//background.mp3
MoviePy - Done.
Moviepy - Building video C:\Users\Administrator\Desktop\job\video\—来自：音乐榜单的第7个音乐《晚风遇见你（副歌版）》第6页第10个@宸宸不挑食 的作品3.mp4.
MoviePy - Writing audio in —来自：音乐榜单的第7个音乐《晚风遇见你（副歌版）》第6页第10个@宸宸不挑食 的作品3TEMP_MPY_wvf_snd.mp3
MoviePy - Done.
Moviepy - Writing video C:\Users\Administrator\Desktop\job\video\—来自：音乐榜单的第7个音乐《晚风遇见你（副歌版）》第6页第10个@宸宸不挑食 的作品3.mp4

t: 100%|█████████▉| 854/855 [00:52<00:00, 17.05it/s, now=None][2024-01-17 14:32:09,604]-warnings.py-109-MainThread-C:\ProgramData\Miniconda3\envs\job\lib\site-packages\moviepy\video\io\ffmpeg_reader.py:123: UserWarning: Warning: in file C:\Users\Administrator\Desktop\job\video\—来自：音乐榜单的第7个音乐《晚风遇见你（副歌版）》第6页第10个@宸宸不挑食 的作品2.mp4, 6220800 bytes wanted but 0 bytes read,at frame 854/855, at time 28.47/28.47 sec. Using the last valid frame instead.
  warnings.warn("Warning: in file %s, "%(self.filename)+

Moviepy - Done !
Moviepy - video ready C:\Users\Administrator\Desktop\job\video\—来自：音乐榜单的第7个音乐《晚风遇见你（副歌版）》第6页第10个@宸宸不挑食 的作品3.mp4
背景音乐添加完成！
处理后md5： afa391570142c8958d24cc8116b4886b
视频处理完毕
code: 0
[2024-01-17 14:32:13,043]-main.py-571-MainThread-视频下载成功，等待发布
视频下载成功，等待发布
正在判断账号是否登录
账号已登录
该视频有话题
Timeout 30000ms exceeded.
正在添加第1个话题
正在添加第2个话题
正在添加第3个话题
正在添加第4个话题
正在添加第5个话题
正在添加第1个想@的人
@庐陵老街陈万洵失败了，可能被对方拉黑了
[2024-01-17 14:33:05,149]-main.py-482-MainThread-@庐陵老街陈万洵失败了，可能被对方拉黑了
正在添加第2个想@的人
想@的人 宸宸不挑食
正在添加第6个话题
视频标题输入完毕，等待发布
来自网页的实时消息：请等待视频上传成功
```

# 声明
- qq交流群：916790180
- 有任何问题请到[issues](https://github.com/Superheroff/douyin_uplod/issues)提交
- 本源码只是出于学习交流的目的，使用者造成的任何后果均与作者无关
