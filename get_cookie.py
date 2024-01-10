# -*- coding: utf-8 -*-
"""
@Time    : 2024/1/10 22:11
@Author  : superhero
@Email   : 838210720@qq.com
@File    : get_cookie.py
@IDE: PyCharm
"""

import asyncio
import os
import json
import requests
from playwright.async_api import Playwright, async_playwright


def get_phone_city(number):
    ret = requests.get("https://cx.shouji.360.cn/phonearea.php?number=%s" % number).json()
    # print(ret)
    city = ret["data"].get("city", "")
    province = ret["data"].get("province", "")
    if not city:
        city = province + "市"
    else:
        city = city + "市"
    if province and city:
        province = province + "省"
    return city, province


class creator_douyin():
    def __init__(self, phone, timeout: int):
        """
        初始化
        :param phone: 手机号
        :param timeout: 你要等待多久，单位秒
        """
        self.timeout = timeout * 1000
        self.phone = phone
        self.path = os.path.abspath('')
        text = "cookie"
        self.desc = "%s_%s.json" % (text, self.phone)
        self.is_v = True
        file_path = os.path.join(self.path, "proxy.ini")
        self.chrome_path = r"\chromium-1055\chrome-win\chrome.exe"
        # work = load_workbook(self.path + r'\province-and-city.xlsx')
        # worksheet = work['Sheet1']
        # self.province_list = []
        # self.city_list = []
        # self.pid_list = []
        # self.cid_list = []
        # for row_cell in worksheet['A4':'D%s' % worksheet.max_row]:
        #     self.pid_list.append(row_cell[2].value)
        #     self.cid_list.append(row_cell[0].value)
        #     self.province_list.append(row_cell[3].value)
        #     self.city_list.append(row_cell[1].value)

        city, province = get_phone_city(self.phone)
        print("省份：%s" % province + "，城市：%s" % city)
        # with open(self.path + "\\city_encoding.txt", mode="r", encoding="utf-8") as f:
        #     city_encoding = json.loads(f.read())
        #     self.province = city_encoding.get(province, "")
        #     self.city = str(city_encoding.get(city, ""))

        # if os.path.exists(file_path):
        #     conn = ConfigParser()
        #     conn.read(file_path)
        #     self.proxy_host = conn.get('set', 'proxy_host')
        #     self.proxy_user = conn.get('set', 'proxy_user')
        #     self.proxy_password = conn.get('set', 'proxy_password')
            # self.url = conn.get('root', 'url')
        i = 0
        while True:
            i += 1
            if os.path.exists(self.path + "\\" + self.desc):
                text = "cookie(%s)" % i
                self.desc = "%s_%s.json" % (text, self.phone)

            else:
                # open(self.path + "\\" + self.desc, mode="w")
                #  os.mknod(self.path + "\\" + self.desc)
                #  mknod 不支持windows
                break

    # def get_proxy(self):
    #     ret = requests.get(self.url + "&province=%s&city=%s" % (self.province, self.city)).json()
    #     try:
    #         proxy = ret['list'][0]['sever'] + ":" + str(ret['list'][0]['port'])
    #         print("当前代理IP：%s" % proxy)
    #     except Exception:
    #         print("代理获取失败，请检查是否加入白名单，如果继续操作本次将不使用代理")
    #         return ""
    #     return proxy

    async def __cookie(self, playwright: Playwright) -> None:
        # proxy = self.get_proxy()
        # if self.proxy_host and self.proxy_user and self.proxy_password:
        #     browser = await playwright.chromium.launch(channel="chrome", headless=False,
        #                                                executable_path=self.path + self.chrome_path,
        #                                                proxy={
        #                                                    "server": self.proxy_host,
        #                                                    "username": self.proxy_user,
        #                                                    "password": self.proxy_password
        #                                                }
        #                                                )
        # else:
        browser = await playwright.chromium.launch(channel="chrome", headless=False,
                                                   # executable_path=self.path + self.chrome_path
                                                   )

        context = await browser.new_context()

        page = await context.new_page()
        await page.add_init_script("Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});")

        await page.goto("https://creator.douyin.com/")

        await page.locator(
            "div.banner-div:nth-child(1) > div:nth-child(1) > img:nth-child(1)").click()

        await page.locator("div.semi-tabs-tab:nth-child(2)").click()

        await page.locator('input.semi-input:nth-child(2)').fill(self.phone)
        try:
            await page.wait_for_url("https://creator.douyin.com/creator-micro/home", timeout=self.timeout)
            self.is_v = True
        except Exception:
            self.is_v = False
            print("登录失败，本次操作不保存cookie")
        # await page.wait_for_timeout(3000)
        cookies = await context.cookies()
        cookie_txt = ''
        for i in cookies:
            cookie_txt += i.get('name') + '=' + i.get('value') + '; '
        print("cookie", cookie_txt)
        if self.is_v:
            with open(self.path + "\\" + self.phone + ".txt", mode="w") as f:
                f.write(cookie_txt)
            await context.storage_state(path=self.path + "\\" + self.desc)
        await context.close()
        await browser.close()

    async def main(self):
        async with async_playwright() as playwright:
            await self.__cookie(playwright)


def main():
    while True:
        phone = input('请输入手机号码\n输入"exit"将退出服务\n')
        if phone == "exit":
            break
        elif phone.isnumeric() and len(phone) == 11:
            app = creator_douyin(phone, 60)
            asyncio.run(app.main())
        else:
            print('请输入正确的手机号码\n')


main()
