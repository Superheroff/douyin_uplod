# -*- coding: utf-8 -*-
from playwright.async_api import Playwright, async_playwright
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime
import requests
from xml.etree import ElementTree
import wave
from ffmpy import FFmpeg
import os
import asyncio


class set_video(object):
    def __init__(self):
        self.text = ''  # 视频标题
        self.tp = 0  # 存储单双号
        self.path = r'C:\Users\Administrator\Desktop\windows\audio'  # 资源目录

    def s_video(self):
        """
        构建视频信息，音频、标题等
        :return:
        """
        times = datetime.datetime.now()
        _date = str(times.year) + '-' + str(times.month).zfill(2) + '-' + str(times.day).zfill(2)
        if times.day % 2 == 0:
            self.tp = 0
            url = 'http://api.yanxi520.cn/api/xljtwr.php?charset=utf-8'
            t = '，今天又是愉快的一天。'
        else:
            t = '，今天又是舔狗的一天。'
            self.tp = 1
            url = 'http://api.yanxi520.cn/api/tiangou.php'

        while True:
            text = requests.get(url).text
            print(text)
            if len(text) > 18:  # 字数太短了重新获取
                break
        if text:
            self.text = text
            self.g_audio()
        self.text = _date + t + '%s  -来自：小卤蛋机器人自动合成并发布' % text

    def g_video(self):
        """
        生成视频
        :return:
        """
        # 传入的视频路径
        video_path = self.path + '\\temp2.mp4' if self.tp == 0 else self.path + '\\temp.mp4'
        # 传入的音频路径
        audio_path = self.path + '\\temp.wav'
        # 生成的视频名称
        output_path = self.path + '\\temps.mp4'
        if os.path.exists(output_path):
            os.remove(output_path)

        ff = FFmpeg(
            inputs={video_path: None, audio_path: None},
            outputs={output_path: '-map 0:v -map 1:a -c:v copy -c:a aac -shortest'},
            global_options='-stream_loop -1',  # 全局参数 视频时长小于音乐时长时将循环视频
            executable=r'E:\ffmpeg\ffmpeg-5.0.1-essentials_build\bin\ffmpeg.exe'
        )

        ff.run()


class set_audio(set_video):
    def __init__(self):
        super(set_audio, self).__init__()

    def g_audio(self):
        """
        生成音频
        :return:
        """
        uri = 'https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        apiKey = ""  # 微软云key
        header = {
            'Ocp-Apim-Subscription-Key': apiKey,
            'Host': 'eastus.api.cognitive.microsoft.com',
            'Content-type': 'application/x-www-form-urlencoded',
            'Content-Length': '0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        accesstoken = requests.post(uri, headers=header).text
        print("Access Token: " + accesstoken)

        if self.tp == 0:
            voice_name = 'Xiaoxiao'
            style = 'chat'
            background_url = 'https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/7109718515510217509.mp3'
        else:
            voice_name = 'Yunxi'
            style = 'narration-relaxed'
            background_url = 'https://sf3-cdn-tos.douyinstatic.com/obj/tos-cn-ve-2774/a7cb287d9da34c1e98f45938f11f93c8'
        body = ElementTree.Element('speak', version='1.0')
        body.set('xmlns', 'http://www.w3.org/2001/10/synthesis')
        body.set('xmlns:mstts', 'http://www.w3.org/2001/mstts')
        body.set('xmlns:emo', 'http://www.w3.org/2009/10/emotionml')
        body.set('xml:lang', 'zh-CN')
        background = ElementTree.SubElement(body, 'mstts:backgroundaudio')
        # https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/7109718515510217509.mp3
        # https://sf3-cdn-tos.douyinstatic.com/obj/tos-cn-ve-2774/a7cb287d9da34c1e98f45938f11f93c8
        background.set('src', background_url)  # 设置背景音乐
        background.set('volume', '0.2')  # 设置背景音乐 音量
        background.set('fadein', '2000')  # 设置背景音乐 淡入
        background.set('fadeout', '3000')  # 设置背景音乐 淡出
        voice = ElementTree.SubElement(body, 'voice')

        voice.set('name', 'zh-CN-%sNeural' % voice_name)
        mstts = ElementTree.SubElement(voice, 'mstts:express-as')
        mstts.set('style', style)
        prosody = ElementTree.SubElement(mstts, 'prosody')
        prosody.set('rate', '-10%')
        prosody.text = self.text
        # print('self.text', self.text)

        header = {"Content-type": "application/ssml+xml",
                  "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
                  "Authorization": "Bearer " + accesstoken,
                  "User-Agent": "TTSForPython"}

        uri = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'
        res = requests.post(uri, data=ElementTree.tostring(body), headers=header).content
        # with open(self.path + "\\temp.wav", "wb") as f:
        #     f.write(res)
        f = wave.open(self.path + "\\temp.wav", "wb")
        f.setnchannels(1)  # 单声道
        f.setframerate(24000)  # 采样率
        f.setsampwidth(2)  # sample width 2 bytes(16 bits)
        f.writeframes(res)
        f.close()


class pw(set_audio):
    def __init__(self):
        super(pw, self).__init__()

    async def upload(self, playwright: Playwright) -> None:
        browser = await playwright.chromium.launch(headless=False)

        context = await browser.new_context(storage_state=self.path + "\\cookie.json")

        page = await context.new_page()

        await page.goto("https://creator.douyin.com/creator-micro/content/upload")

        await page.locator("button:has-text(\"发布视频\")").click()
        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/upload")

        await page.locator(
            "label:has-text(\"点击上传 或直接将视频文件拖入此区域为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").set_input_files(
            "temps.mp4")

        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/publish")
        time.sleep(20)

        await page.locator('xpath=//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div/div[1]/div[1]/div').fill(
            self.text)
        # 视频越大间隔应越长
        time.sleep(30)
        await page.locator(
            'xpath=//*[@id="root"]//div/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        await page.wait_for_timeout(6000)

        await context.storage_state(path=self.path + "\\cookie.json")
        await context.close()
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)


def job_1():
    app = pw()
    app.s_video()
    app.g_video()
    asyncio.run(app.main())

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(job_1, 'cron', day='1-31', hour='5', minute='20', misfire_grace_time=180)
    scheduler.start()

