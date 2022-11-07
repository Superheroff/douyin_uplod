# douyin_uplod
- 从0自动生成视频，解决你不知道发什么视频的烦恼。

# 原理
1. 使用apscheduler开启计划任务，每天x点x分运行
2. 通过自定义的文字以及背景音乐合成音频【使用了微软语音合成】
3. 通过音频和临时视频片段合成视频【使用了ffmpeg】
4. 抖音的上传是用了aws4加密这个其实也可以通过协解密来完成，但是代码量就多了，不符合学习的目的

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
# 结尾
qq交流群：916790180
本源码只是出于学习交流的目的，非法使用与作者无关
