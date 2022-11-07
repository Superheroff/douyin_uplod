# douyin_uplod
**抖音自动上传视频**
- 可以实现定时自动上传自定义视频或者重新造一个视频上传
- 原理：通过自定义的文字合成音频并与短片或者图片以及背景音乐合成一个完整的视频然后通过playwright去操作上传


# 技术栈
- python
- playwright
- ffmpeg
- apscheduler

# 前期准备
- 需要通过playwright录制脚本命令扫码登录后把cookie文件保存下来
- 准备至少2个临时视频片段，最好可以循环重复的静音视频
```
playwright codegen www.douyin.com --save-storage=cookie.json
```
