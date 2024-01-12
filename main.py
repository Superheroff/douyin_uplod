import asyncio
import hashlib
import logging
import random
import re
import time

import cv2
import pandas as pd
import requests
from PIL import Image
from apscheduler.schedulers.blocking import BlockingScheduler
from ffmpy import FFmpeg
from moviepy.editor import *
from playwright.async_api import Playwright, async_playwright

import config
from config import conigs
from logs import config_log


def get_file_md5(file_path):
    """
    取文件md5
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        content = file.read()
    md5_obj = hashlib.md5()
    md5_obj.update(content)
    return md5_obj.hexdigest()


def merge_images_video(image_folder, output_file, video_path, fps=None):
    """
    把图片合并成视频并添加背景音乐
    :param image_folder: 图片文件夹路径
    :param output_file: 输出视频文件路径
    :param video_path: 待提取背景音乐的视频文件路径
    :param fps:
    :return:
    """
    # 获取文件夹内所有图片的列表
    image_list = os.listdir(image_folder)
    # 获取图片总数量
    index = len(image_list)

    # 获取第一张图片的大小作为视频分辨率
    first_img = Image.open(image_folder + image_list[0])
    if fps is None:
        fps = 30
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4格式
        videowrite = cv2.VideoWriter(output_file, fourcc, fps, first_img.size)
        img_array = []
        for filename in [r'./frames/{0}.jpg'.format(i) for i in range(29, index + 29)]:
            img = cv2.imread(filename)
            if img is None:
                print("is error!")
                continue
            img_array.append(img)
        # 合成视频
        for i in range(1, len(img_array)):
            img_array[i] = cv2.resize(img_array[i], first_img.size)
            videowrite.write(img_array[i])
            print('第{}张图片合成成功'.format(i))
        # 关闭视频流
        videowrite.release()

        print('开始添加背景音乐！')
        # 从某个视频中提取一段背景音乐
        audio_sample_rate = 48000
        audio_file = AudioFileClip(video_path, fps=audio_sample_rate)
        # 将背景音乐写入.mp3文件
        output_dir = "music/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            config.delete_all_files(output_dir)
        audio = CompositeAudioClip([audio_file])
        audio.write_audiofile(output_dir + '/background.mp3', fps=audio_sample_rate)
        dd_path = output_file[:-5] + '3.mp4'
        # 2种方案
        # 方案一 使用moviepy，内存更小
        clip = VideoFileClip(output_file)
        clip = clip.set_audio(audio)
        clip.write_videofile(dd_path)

        # 方案二 使用ffmpeg，内存更大
        # ff = FFmpeg(
        #     inputs={output_file: None, output_dir + '/background.mp3': None},
        #     outputs={dd_path: '-map 0:v -map 1:a -c:v copy -c:a aac -shortest'},
        #     global_options='-stream_loop -1',  # 全局参数 视频时长小于音乐时长时将循环视频
        #     # executable=r'E:\易语言\ffmpeg\ffmpeg-5.0.1-essentials_build\bin\ffmpeg.exe'
        # )
        # ff.run()
        print('背景音乐添加完成！')

    except Exception as e:
        print("发生错误：", str(e))
        logging.info(str(e))


def set_video_frame(video_path):
    """
    抽取视频帧，返回fps用于后面合成
    :param video_path: 视频文件路径
    :return:
    """
    # 打开视频文件
    video = cv2.VideoCapture(video_path)

    # 获取视频的帧数、每秒帧数等信息
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)

    # 设置要提取的帧数范围
    start_frame = 29  # 起始帧，剔除前面30帧和结尾20帧
    end_frame = frame_count - 21  # 结束帧

    # 创建保存抽取帧的目录
    output_dir = 'frames/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        config.delete_all_files(output_dir)

    # 定位到指定的起始帧
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 按照指定的间隔提取并保存帧图像
    for i in range(start_frame, end_frame + 1):
        ret, frame = video.read()
        if not ret:
            break
        output_file = f'{output_dir}{i}.jpg'
        cv2.imwrite(output_file, frame)

        print(f"已处理 {i + 1}/{end_frame} 帧")

    print("所有帧都已成功抽取！")
    # 关闭视频流
    video.release()

    merge_images_video(os.path.abspath("") + "\\frames\\", video_path[:-4] + "2.mp4", video_path, fps)


class douyin(object):
    def __init__(self):
        config_log()
        self.title = ""
        self.ids = ""
        self.video_path = ""
        self.page = 0
        self.path = os.path.abspath('')
        self.cid = "d9ba8ae07d955b83c3b04280f3dc5a4a"
        self.ua = {
            "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
                   "Safari/537.36",
            "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
                   "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
        }

    def get_web_cookie(self):
        """
        获取cookie
        :return:
        """
        url = 'http://api2.52jan.com/dyapi/get_cookie/v2'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        resp = requests.post(url, data={'sign': sign}, headers=header).json()
        return resp['data'][0]['cookie']

    def get_appkey(self):
        data = self.cid + '5c6b8r9a'
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def set_sign(self):
        ts = str(time.time()).split('.')[0]
        string = '1005' + self.cid + ts + self.get_appkey()
        sign = hashlib.md5(string.encode('utf8')).hexdigest()
        return sign

    def get_web_xbogus(self, url, ua):
        """
        获取web xbogus
        :param url:
        :param ua:
        :return:
        """
        sign_url = 'http://api2.52jan.com/dyapi/web/xbogus'
        ts = str(time.time()).split('.')[0]
        header = {
            'cid': self.cid,
            'timestamp': ts,
            'user-agent': 'okhttp/3.10.0.12'
        }
        sign = self.set_sign()
        params = {
            'url': url,
            'ua': ua,
            'sign': sign
        }
        resp = requests.post(sign_url, data=params, headers=header).json()
        return resp

    def get_douyin_music(self):
        """
        获取抖音Top50音乐榜单
        :return:
        """
        url = f"https://api3-normal-c-hl.amemv.com/aweme/v1/chart/music/list/?request_tag_from=rn&chart_id=6853972723954146568" \
              f"&count=100&cursor=0&os_api=22&device_type=MI 9" \
              f"&ssmix=a&manifest_version_code=110101&dpi=240&uuid=262324373952550&app_name=aweme&version_name=11.1.0&ts={round(time.time())}" \
              f"&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code" \
              f"=11109900&channel=douyinw&_rticket={round(time.time() * 1000)}&device_platform=android&iid=157935741181076" \
              f"&version_code=110100&cdid=02a0dd0b-7ed3-4bb4-9238-21b38ee513b2&openudid=af450515be7790d1&device_id=3166182763934663" \
              f"&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=Xiaomi&aid=1128&mcc_mnc=46007"

        try:
            res = requests.get(url, headers={"User-Agent": self.ua["app"]}).json()
            x = random.randint(0, len(res["music_list"]) - 1)
            music_list = res["music_list"][x]
            self.title = f"—来自：音乐榜单的第{(x + 1)}个音乐《{music_list['music_info']['title']}》"
            self.ids = music_list["music_info"]["id_str"]
            return self.get_filter()
        except Exception:
            logging.info("获取抖音Top50音乐榜单失败")
            return 2

    def get_douyin_music_video(self, music_id=None):
        """
        根据音乐id获取音乐视频列表
        :param music_id:
        :return:
        """

        if music_id is None:
            music_id = self.ids if self.ids else "7315704709279550259"

        pages = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        self.page = random.choice(pages)

        url = f"https://www.douyin.com/aweme/v1/web/music/aweme/?device_platform=webapp&aid=6383&channel" \
              f"=channel_pc_web&count=10&cursor={self.page}&music_id={music_id}&pc_client_type=1&version_code=170400" \
              f"&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN" \
              f"&browser_platform=Win32&browser_name=Chrome&browser_version=120.0.0.0&browser_online=true&engine_name" \
              f"=Blink&engine_version=120.0.0.0&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform" \
              f"=PC&downlink=10&effective_type=4g&round_trip_time=50"

        headers = {
            "Host": "www.douyin.com",
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": self.ua["web"],
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.douyin.com/music/" + music_id,
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.get_web_cookie()
        }
        xbogus = self.get_web_xbogus(url, self.ua["web"])
        url += '&X-Bogus=' + xbogus['xbogus']
        try:
            res = requests.get(url, headers=headers).json()
            verify_reason_values = []
            video_duration_values = []
            remove_custom_verify = []
            # 这里把要筛选的条件值加入到筛选列表当中
            for i in res["aweme_list"]:
                verify_reason_values.append(i["author"]["enterprise_verify_reason"])
                video_duration_values.append(i["video"]["duration"])
                remove_custom_verify.append(i["author"]["custom_verify"])
            verify_reason = {
                "verify_reason": verify_reason_values,
                "duration": video_duration_values,
                "custom_verify": remove_custom_verify
            }
            df = pd.DataFrame(verify_reason)
            if conigs.remove_enterprise and conigs.remove_images and conigs.remove_custom_verify:
                # 判断是否满足所有条件
                jd = df[(df['verify_reason'] == "") & (df['duration'] >= (conigs.duration * 1000)) & (
                            df['custom_verify'] == "")]
                # 判断是否有满足条件的数据
                if len(jd.index.values) > 0:
                    return jd, res
                else:
                    return 101, "所有都条件不满足"
            else:
                return 200, res
        except Exception as e:
            print("出现错误：", e)
            logging.info(e)
            return 1, "1"

    def get_filter(self):
        """
        使用pands过滤数据
        :return:
        """
        while True:
            jd, res = self.get_douyin_music_video()
            if type(jd) != type(101):
                break
            elif jd == 101:
                print("所有都条件不满足")

        if type(jd) != type(101):
            dd = jd.sample()
            # print(dd.index.values)
            index = dd.index.values[0]
            video_list = res['aweme_list'][index]
        elif jd == 1:
            return jd
        else:
            index = random.randint(0, len(res['aweme_list']) - 1)
            video_list = res['aweme_list'][index]

        uri = video_list["video"]["play_addr_h264"]["url_list"][0]
        nickname = video_list['author']['nickname']
        # print(json.dumps(video_list))
        print("url:", uri)
        print("nickname:", nickname)

        # 获取自定义的视频标题
        page_index = 1 if self.page == 0 else round(self.page / 10 + 1)
        self.title += f"第{page_index}页第{index + 1}个@{nickname} 的作品"

        desc = random.choice(conigs.video_title_list) if conigs.title_random else ''.join(
            conigs.video_title_list)
        desc += ''.join(conigs.video_at) + self.title
        reb = requests.get(uri, headers={"User-Agent": self.ua["web"]}).content
        self.video_path = conigs.video_path + desc + ".mp4"
        with open(self.video_path, mode="wb") as f:
            f.write(reb)
            print("处理前md5：", get_file_md5(self.video_path))
            print("正在处理视频")
            # clip = VideoFileClip(self.video_path)
            # clip.subclip(10, 20)  # 剪切
            set_video_frame(self.video_path)
            # self.video_path这个文件名不能改，上传就是上传这个
            self.video_path = conigs.video_path + desc + "3.mp4"
            # clip.write_videofile(self.video_path)  # 保存视频
            print("处理后md5：", get_file_md5(self.video_path))
            print("视频处理完毕")
        return 0


class upload_douyin(douyin):
    def __init__(self, timeout: int, cookie_file: str):
        super(upload_douyin, self).__init__()
        """
        初始化
        :param timeout: 你要等待多久，单位秒
        :param cookie_file: cookie文件路径
        """
        self.timeout = timeout * 1000
        self.cookie_file = cookie_file

    async def upload(self, playwright: Playwright) -> None:

        browser = await playwright.chromium.launch(channel="chrome", headless=False)

        context = await browser.new_context(storage_state=self.cookie_file, user_agent=self.ua["web"])

        page = await context.new_page()
        await page.add_init_script("Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});")

        print("正在判断账号是否登录")
        try:
            await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            await page.locator(".login").click(timeout=1500)
            print("未登录，正在跳出")
            logging.info("未登录，正在跳出")
            is_login = False
        except Exception as e:
            # print("出现此error，代表cookie正常反之异常\n", e)
            is_login = True
            print("账号已登录")
        if is_login:
            try:
                await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            except Exception as e:
                print("发布视频失败，cookie已失效，请登录后再试\n", e)
                logging.info("发布视频失败，cookie已失效，请登录后再试")

            video_desc_list = self.video_path.split("\\")
            video_desc = str(video_desc_list[len(video_desc_list) - 1])[:-4]

            video_desc_tag = []
            tag_rs = re.findall(r"(#.*?) ", video_desc)
            if len(tag_rs) > 0:
                video_desc_tag = video_desc.split(" ")
                print("该视频有话题")
            else:
                video_desc_tag.append(video_desc)
                print("该视频没有检测到话题")

            try:
                async with page.expect_file_chooser() as fc_info:
                    await page.locator(
                        "label:has-text(\"点击上传 或直接将视频文件拖入此区域为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(self.video_path, timeout=self.timeout)
            except Exception as e:
                print("发布视频失败，可能网页加载失败了\n", e)
                logging.info("发布视频失败，可能网页加载失败了")
            # await page.locator("label:has-text(\"点击上传 或直接将视频文件拖入此区域为了更好的观看体验和平台安全，平台将对上传的视频预审。超过40秒的视频建议上传横版视频\")").set_input_files("下载.mp4", timeout=self.timeout)
            try:
                await page.locator(".modal-button--38CAD").click()
            except Exception as e:
                print(e)
            await page.wait_for_url("https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page")
            # css视频标题选择器

            css_selector = ".zone-container"
            await page.locator(".ace-line > div").click()
            tag_index = 0
            at_index = 0
            # 处理末尾标题
            video_desc_end = len(video_desc_tag) - 1
            video_desc_tag[video_desc_end] = video_desc_tag[video_desc_end][:-1]
            for tag in video_desc_tag:
                await page.type(css_selector, tag)
                if "@" in tag:
                    at_index += 1
                    print("正在添加第%s个想@的人" % at_index)
                    time.sleep(3)
                    try:
                        if len(conigs.video_at2) <= at_index:
                            await page.get_by_text("抖音号 %s" % conigs.video_at2[at_index - 1]).click(timeout=5000)
                        else:
                            await page.get_by_text(tag[1:], exact=True).first.click(timeout=5000)
                    except Exception as e:
                        print(tag + "失败了", e)
                        logging.info(tag + "失败")

                else:
                    tag_index += 1
                    await page.press(css_selector, "Space")
                    print("正在添加第%s个话题" % tag_index)
            print("视频标题输入完毕，等待发布")
            time.sleep(2)
            # 添加位置信息
            try:
                city = random.choice(conigs.city_list)
                await page.get_by_text("输入地理位置").click()
                time.sleep(3)
                await page.get_by_role("textbox").nth(1).fill(city)
                # await page.get_by_text(conigs.city).click()
                # page.locator("div").filter(has_text=re.compile(r"^位置庐陵老街$")).get_by_role("textbox").fill("庐陵老街")
                await page.locator(".detail-v2--3LlIL").first.click()
            except Exception as e:
                print("位置添加失败")
                logging.info("位置添加失败")

            try:
                await page.locator('button.button--1SZwR:nth-child(1)').click()
            except Exception as e:
                print(e)
            # 获取点击按钮消息
            msg = await page.locator('//*[@class="semi-toast-content-text"]').all_text_contents()
            for msg_txt in msg:
                print("来自网页的实时消息：" + msg_txt)

            # 跳转成功页面
            try:
                await page.wait_for_url("https://creator.douyin.com/creator-micro/content/manage")
                print("账号发布视频成功")
                logging.info("账号发布视频成功")
            except Exception as e:
                is_while = False
                while True:
                    # 循环获取点击按钮消息
                    time.sleep(2)
                    try:
                        await page.locator('button.button--1SZwR:nth-child(1)').click()
                    except Exception as e:
                        print(e)
                        break
                    msg = await page.locator('//*[@class="semi-toast-content-text"]').all_text_contents()
                    for msg_txt in msg:
                        print("来自网页的实时消息：" + msg_txt)
                        if msg_txt == '发布成功':
                            is_while = True
                            logging.info("账号发布视频成功")
                            print("账号发布视频成功")
                        elif msg_txt == '上传成功':
                            try:
                                await page.locator('button.button--1SZwR:nth-child(1)').click()
                            except Exception as e:
                                print(e)
                                break
                            msg2 = await page.locator(
                                '//*[@class="semi-toast-content-text"]').all_text_contents()
                            for msg2_txt in msg2:
                                if msg2_txt == '发布成功':
                                    is_while = True
                                    logging.info("账号发布视频成功")
                                    print("账号发布视频成功")
                                elif msg2_txt.find("已封禁") != -1:
                                    is_while = True
                                    logging.info("账号视频发布功能已被封禁")
                                    print("账号视频发布功能已被封禁")
                        elif msg_txt.find("已封禁") != -1:
                            is_while = True
                            print("视频发布功能已被封禁")
                            logging.info("视频发布功能已被封禁")
                        else:
                            pass

                    if is_while:
                        break

        await context.close()
        await browser.close()

    async def main(self):
        msg = ["视频下载成功，等待发布", "视频下载失败", "音乐榜单获取失败"]
        async with async_playwright() as playwright:
            code = self.get_douyin_music()
            print(code)
            print(msg[code])
            logging.info(msg[code])
            if code == 0:
                await self.upload(playwright)


def run():
    app = upload_douyin(60, conigs.cookie_path)
    asyncio.run(app.main())


if __name__ == '__main__':
    # run()
    # path = r"E:\python\douyin\发布小程序\video\#老赖陈万洵 @1486323920 -来自：榜单的第25个音乐《Love Lee》@超级马立奥 的作品.mp4"
    # set_video_frame(path)
    # merge_images_video(os.path.abspath("") + "\\frames\\", path[:-4] + "2.mp4", path)

    print("调度任务开始运行")
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(run, 'interval', minutes=30, misfire_grace_time=900)
    scheduler.start()
