# douyin_uplod
- 从0自动生成发布视频，解决你不知道发什么视频的烦恼。
- demo的实例是每天5点20分，单号生成并发送舔狗日记，双号生成并发送心灵鸡汤。你们可以根据自己的需求修改下。
- 示例[抖音号](https://v.douyin.com/rA1gERo/)

# 原理
1. 使用apscheduler开启计划任务，每天x点x分运行
2. 通过自定义的文字以及背景音乐合成音频【使用了微软语音合成】
3. 通过音频和临时视频片段合成视频【使用了ffmpeg】
4. 通过playwright发布合成的视频

# 技术栈
- python
- playwright
- ffmpeg
- apscheduler

# 前期准备
- 微软[azure注册](https://azure.microsoft.com/zh-cn/products/cognitive-services/text-to-speech/)
- 没有海外卡的同学，淘宝搜索`微软azure注册`
- 准备至少2个临时视频片段，最好可以循环重复的静音视频
- 安装python
- 安装playwright、ffmpeg、apscheduler，执行以下命令
- 下载[ffmpeg](http://ffmpeg.org/download.html)

```python
pip install apscheduler
pip install ffmpy
pip install playwright
python -m playwright install
```
- 然后通过playwright把cookie文件保存下来，执行以下命令，扫码登录完成后即可

```python
playwright codegen www.douyin.com --save-storage=cookie.json
```
- ffmpeg需要添加到环境变量，如不添加需要修改`ffmpeg.exe`目录`ctrl+左键点击ffmpeg`进入，把`executable='ffmpeg.exe'`修改成你`下载ffmpeg`的目录

```python
def __init__(
        self, executable=r'E:\ffmpeg\ffmpeg-5.0.1-essentials_build\bin\ffmpeg.exe', global_options=None, inputs=None, outputs=None
    )
```
# 结尾
- qq交流群：916790180
- 本源码只是出于学习交流的目的，非法使用发送不良视频等与作者无关
