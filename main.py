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
# from ffmpy import FFmpeg
from moviepy.editor import *
from playwright.async_api import Playwright, async_playwright

from tqdm import tqdm
from config import conigs
from logs import config_log
from datetime import datetime


def delete_all_files(folder_path):
    # 获取文件夹中所有文件的列表
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        # 判断是否为文件
        if os.path.isfile(file_path):
            # 删除文件
            os.remove(file_path)


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


async def merge_images_video(image_folder, output_file, video_path, fps=None):
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
    first_img = Image.open(os.path.join(image_folder, image_list[0]))
    if fps is None:
        fps = 30
    try:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4格式
        videowrite = cv2.VideoWriter(output_file, fourcc, fps, first_img.size)
        img_array = []

        start_frame = conigs.start_frame

        for filename in [f'./frames/{i}.jpg' for i in range(start_frame, index + start_frame)]:
            img = cv2.imread(filename)
            if img is None:
                print("is error!")
                continue
            img_array.append(img)
        # 合成视频
        with tqdm(total=len(img_array), desc="图片合成进度") as pbar:
            for i in range(len(img_array)):
                img_array[i] = cv2.resize(img_array[i], first_img.size)
                videowrite.write(img_array[i])
                pbar.update(1)
                # print('第{}张图片合成成功'.format(i))
        # 关闭视频流
        videowrite.release()

        print('开始添加背景音乐！')
        # 从某个视频中提取一段背景音乐
        fps = 48000
        audio_file = AudioFileClip(video_path, fps=fps)
        # 将背景音乐写入.mp3文件
        output_dir = "music/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            delete_all_files(output_dir)
        audio = CompositeAudioClip([audio_file])
        audio.write_audiofile(os.path.join(output_dir, "background.mp3"), fps=fps)
        dd_path = output_file[:-5] + "3.mp4"
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
        print("发生错误：", e)
        logging.info(e)


async def set_video_frame(video_path):
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
    start_frame = conigs.start_frame - 1  # 起始帧
    end_frame = frame_count - (conigs.end_frame + 1)  # 结束帧

    # 创建保存抽取帧的目录
    output_dir = 'frames/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        delete_all_files(output_dir)

    # 定位到指定的起始帧
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # 按照指定的间隔提取并保存帧图像
    with tqdm(total=(end_frame - start_frame), desc="视频抽帧进度") as pbar:
        for i in range(start_frame + 1, end_frame + 1):
            ret, frame = video.read()
            if not ret:
                break
            output_file = os.path.join(output_dir, f"{i}.jpg")
            cv2.imwrite(output_file, frame)
            pbar.update(1)
            # print(f"已处理 {i + 1}/{end_frame + 1} 帧")

    # print("所有帧都已成功抽取！")
    # 关闭视频流
    video.release()
    await merge_images_video(os.path.join(os.path.abspath(""), "frames"), video_path[:-4] + "2.mp4", video_path, fps)


class douyin():
    def __init__(self):
        config_log()
        self.title = ""
        self.ids = ""
        self.video_path = ""
        self.video_ids = []
        self.page = 0
        self.path = os.path.abspath('')
        self.ua = {
            "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 "
                   "Safari/537.36",
            "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
                   "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
        }
        if not os.path.exists(conigs.video_path):
            os.makedirs(conigs.video_path)
        if conigs.remove_video:
            delete_all_files(conigs.video_path)
            delete_all_files(os.path.join(self.path, "frames"))

    async def playwright_init(self, p: Playwright, headless=None):
        """
        初始化playwright
        """
        if headless is None:
            headless = False

        browser = await p.chromium.launch(headless=headless,
                                          chromium_sandbox=False,
                                          ignore_default_args=["--enable-automation"],
                                          channel="chrome"
                                          )
        return browser

    async def get_douyin_music(self):
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

        res = requests.get(url, headers={"User-Agent": self.ua["app"]}).json()
        x = random.randint(0, len(res["music_list"]) - 1)
        music_list = res["music_list"][x]
        self.title = f"—来自：音乐榜单的第{(x + 1)}个音乐《{music_list['music_info']['title']}》"
        self.ids = music_list["music_info"]["id_str"]
        print("music_id:", self.ids)
        try:
            await self.get_filter()
        except Exception as e:
            logging.info("根据音乐ID获取视频失败", e)

    def get_web_userinfo(self, unique_id) -> str:
        """
        根据抖音号获取用户信息
        :param unique_id:
        :return:
        """
        url = "https://www.iesdouyin.com/web/api/v2/user/info/?unique_id={}".format(unique_id)
        res = requests.get(url, headers={"User-Agent": self.ua["web"]}).json()
        n = 0
        while True:
            n += 1
            try:
                nickname = res["user_info"]["nickname"]
                break
            except KeyError:
                print("获取用户昵称失败！")
            if n > 3:
                nickname = ''
                break
        return nickname

    async def get_douyin_music_video(self, p: Playwright, music_id=None):
        """
        根据音乐id获取音乐视频列表
        :return:
        """

        if music_id is None:
            music_id = self.ids if self.ids else "7315704709279550259"

        browser = await self.playwright_init(p, headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.add_init_script(path="stealth.min.js")
        await page.goto("https://www.douyin.com/music/" + music_id)

        pages = []
        for x in range(0, 40):
            pages.append(x * 10)

        self.page = random.choice(pages)

        url = (f"https://www.douyin.com/aweme/v1/web/music/aweme/?device_platform=webapp&aid=6383&channel"
               f"=channel_pc_web&count=12&cursor={self.page}&music_id={music_id}&pc_client_type=1&version_code=170400"
               f"&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1280&browser_language=zh-CN"
               f"&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true"
               f"&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=32"
               f"&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100"
               )

        res = await page.evaluate("""() => {
            function queryData(url) {
               var p = new Promise(function(resolve,reject) {
                   var e={
                           "url":"%s",
                           "method":"GET"
                         };
                    var h = new XMLHttpRequest;
                    h.responseType = "json";
                    h.open(e.method, e.url, true);
                    h.setRequestHeader("Accept","application/json, text/plain, */*");
                    h.setRequestHeader("Host","www.douyin.com"); 
                    h.setRequestHeader("Referer","https://www.douyin.com/music/%s"); 
                    h.setRequestHeader("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36");   
                    h.onreadystatechange = function() {
                         if(h.readyState === 4 && h.status === 200) {
                              resolve(h.response);
                         } else {}
                    };
                    h.send(null);
                    });
                    return p;
                }
            var p1 = queryData();
            res = Promise.all([p1]).then(function(result){
                    return result
            })
            return res
        }""" % (url, music_id))

        try:
            res = res[0]

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
                    dd = jd.sample()
                    # print(dd.index.values)
                    index = dd.index.values[0]
                    video_list = res['aweme_list'][index]
                    return video_list
                else:
                    return "所有都条件不满足"
            else:
                index = random.randint(0, len(res['aweme_list']) - 1)
                video_list = res['aweme_list'][index]
                return video_list
        except Exception as e:
            logging.info(e)
            return "error"

    async def get_filter(self):
        """
        使用pands过滤数据
        :return:
        """
        for i in range(1, 5):
            async with async_playwright() as p:
                res = await self.get_douyin_music_video(p)
            if isinstance(res, dict):
                if conigs.remove_enterprise and conigs.remove_images and conigs.remove_custom_verify:
                    aweme_id = res['aweme_id']
                    with open(os.path.join(self.path, "video_id_list.txt"), encoding="utf-8", mode="r") as f:
                        self.video_ids = f.read().split(",")
                    if aweme_id not in self.video_ids:
                        self.video_ids.append(aweme_id)
                        break
                    else:
                        print(f"该视频:{aweme_id}已经发送过了本次不再发送")
                else:
                    break
            elif isinstance(res, str):
                print(res)
        if res == 'error': return
        aweme_id = res['aweme_id']
        uri = res["video"]["play_addr_h264"]["url_list"][0]
        nickname = res['author']['nickname']
        # print(json.dumps(video_list))
        print("url:", uri)
        print("nickname:", nickname)
        print("video_id:", aweme_id)

        # 获取自定义的视频标题
        page_index = 1 if self.page == 0 else round(self.page / 12 + 1)
        self.title += f"第{page_index}页@{nickname} 的作品"

        day = datetime.now().day
        if conigs.today:
            # video_title_list = video_title_list2 if day % 2 == 0 else video_title_list1
            if day % 2 == 0:
                conigs.title_random = False
                video_title_list = conigs.video_title_list2
            else:
                video_title_list = conigs.video_title_list1
        else:
            video_title_list = conigs.video_title_list1

        if not conigs.title_random:
            if len(video_title_list) > 5:
                print("错误，话题数不能大于5")
        desc = random.choice(video_title_list) if conigs.title_random else ''.join(
            video_title_list)

        nickname = ''
        for at in conigs.video_at:
            nickname += f"@{self.get_web_userinfo(at)} "
        desc += nickname + self.title
        reb = requests.get(uri, headers={"User-Agent": self.ua["web"]}).content
        self.video_path = os.path.join(conigs.video_path, desc + ".mp4")
        with open(self.video_path, mode="wb") as f:
            f.write(reb)
            print("处理前md5：", get_file_md5(self.video_path))
            print("正在处理视频")
            # clip = VideoFileClip(self.video_path)
            # clip.subclip(10, 20)  # 剪切
            await set_video_frame(self.video_path)
            # self.video_path这个文件名不能改，上传就是上传这个
            self.video_path = os.path.join(conigs.video_path, desc + "3.mp4")
            # clip.write_videofile(self.video_path)  # 保存视频
            print("处理后md5：", get_file_md5(self.video_path))
            print("视频处理完毕")
            with open(os.path.join(self.path, "video_id_list.txt"), encoding="utf-8", mode="w") as f:
                f.write(",".join(self.video_ids)[1:])


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

    async def upload(self, p: Playwright) -> None:
        browser = await self.playwright_init(p)
        context = await browser.new_context(storage_state=self.cookie_file, user_agent=self.ua["web"])
        page = await context.new_page()
        await page.add_init_script(path="stealth.min.js")
        await page.goto("https://creator.douyin.com/creator-micro/content/upload")
        print("正在判断账号是否登录")
        if "/creator-micro/" not in page.url:
            print("账号未登录")
            logging.info("账号未登录")
            return
        print("账号已登录")
        try:
            # 等待视频处理完毕
            await self.get_douyin_music()

            video_desc_list = self.video_path.split("\\")
            video_desc = str(video_desc_list[len(video_desc_list) - 1])[:-4]
            video_desc_tag = []
            if '#' in video_desc or '@' in video_desc:
                video_desc_tag = video_desc.split(" ")
                print("该视频有话题或需要@人")
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

            try:
                await page.locator(".modal-button--38CAD").click()
            except Exception as e:
                print(e)
            await page.wait_for_url(
                "https://creator.douyin.com/creator-micro/content/publish?enter_from=publish_page")
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
                        if len(conigs.video_at) >= at_index:
                            await page.get_by_text("抖音号 " + conigs.video_at[at_index - 1]).click(
                                timeout=5000)
                        else:
                            tag_at = re.search(r"@(.*?) ", tag + " ").group(1)
                            print("想@的人", tag_at)
                            await page.get_by_text(tag_at, exact=True).first.click(timeout=5000)
                    except Exception as e:
                        print(tag + "失败了，可能被对方拉黑了")
                        logging.info(tag + "失败了，可能被对方拉黑了")

                else:
                    tag_index += 1
                    await page.press(css_selector, "Space")
                    print("正在添加第%s个话题" % tag_index)
            print("视频标题输入完毕，等待发布")

            # 添加位置信息，只能添加当地
            if conigs.city:
                time.sleep(2)
                try:
                    city = random.choice(conigs.city_list)
                    await page.get_by_text("输入地理位置").click()
                    time.sleep(3)
                    await page.get_by_role("textbox").nth(1).fill(city)
                    await page.locator(".detail-v2--3LlIL").first.click()
                    print("位置添加成功")
                except Exception as e:
                    logging.info("位置添加失败", e)

            # 添加声明
            if conigs.declaration:
                declaration_int = conigs.declaration_int
                if declaration_int > 6:
                    raise Exception("失败，添加声明序号超出指定范围")
                declaration_content: str = (lambda content, index: content[index])(conigs.declaration_list,
                                                                                   declaration_int - 1)

                await page.locator("p.contentTitle--1Oe95:nth-child(2)").click()
                await page.get_by_role("radio", name=declaration_content, exact=True).click()
                if declaration_int == 1:
                    if len(conigs.declaration_value) < 2:
                        raise Exception("请设置拍摄地和拍摄日期")
                    await page.get_by_text("选择拍摄地点").click()
                    i1 = 0
                    value_list = (conigs.declaration_value[0]).split("-")
                    for i in value_list:
                        if i1 + 1 == len(value_list):
                            await page.locator("li").filter(has_text=i).click()
                        else:
                            await page.locator("li").filter(has_text=i).locator("svg").click()
                        i1 += 1
                    time.sleep(2)
                    await page.get_by_placeholder("设置拍摄日期").click()
                    declaration_value = conigs.declaration_value[1]
                    if declaration_value is None:
                        declaration_value = datetime.today().strftime("-%m-%d")
                    await page.get_by_title(declaration_value).locator("div").click()
                elif declaration_int == 2:
                    await page.get_by_role("radio", name="取材站外", exact=True).click()
                await page.get_by_role("button", name="确定", exact=True).click()

            is_while = False
            while True:
                # 循环获取点击按钮消息
                time.sleep(2)
                try:
                    await page.get_by_role("button", name="发布", exact=True).click()
                    try:
                        await page.wait_for_url("https://creator.douyin.com/creator-micro/content/manage")
                        logging.info("账号发布视频成功")
                        break
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                    break
                msg = await page.locator('//*[@class="semi-toast-content-text"]').all_text_contents()
                for msg_txt in msg:
                    print("来自网页的实时消息：" + msg_txt)
                    if msg_txt.find("发布成功") != -1:
                        is_while = True
                        logging.info("账号发布视频成功")
                        print("账号发布视频成功")
                    elif msg_txt.find("上传成功") != -1:
                        try:
                            await page.locator('button.button--1SZwR:nth-child(1)').click()
                        except Exception as e:
                            print(e)
                            break
                        msg2 = await page.locator(
                            '//*[@class="semi-toast-content-text"]').all_text_contents()
                        for msg2_txt in msg2:
                            if msg2_txt.find("发布成功") != -1:
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



        except Exception as e:
            print("发布视频失败，cookie已失效，请登录后再试\n", e)
            logging.info("发布视频失败，cookie已失效，请登录后再试")
        finally:
            delete_all_files(os.path.join(self.path, "frames"))
            delete_all_files(os.path.join(self.path, "video"))
        # await context.storage_state()

    async def main(self):
        async with async_playwright() as playwright:
            await self.upload(playwright)


def find_file(find_path, file_type) -> list:
    """
    寻找文件
    :param find_path: 子路径
    :param file_type: 文件类型
    :return:
    """
    path = os.path.join(os.path.abspath(""), find_path)
    if not os.path.exists(path):
        os.makedirs(path)
    data_list = []
    for root, dirs, files in os.walk(path):
        if root != path:
            break
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.find(file_type) != -1:
                data_list.append(file_path)
    return data_list


def run():
    cookie_list = find_file("cookie", "json")
    x = 0
    for cookie_path in cookie_list:
        x += 1
        cookie_name: str = os.path.basename(cookie_path)
        print("正在使用[%s]发布作品，当前账号排序[%s]" % (cookie_name.split("_")[1][:-5], str(x)))
        app = upload_douyin(60, cookie_path)
        asyncio.run(app.main())


if __name__ == '__main__':
    run()
    # print("任务开始运行")
    # scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # scheduler.add_job(run, 'interval', minutes=120, misfire_grace_time=900)
    # scheduler.start()
