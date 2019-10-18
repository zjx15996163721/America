#!/usr/bin/env python3
from selenium import webdriver
import time


class Cookie:

        def __init__(self, url):
            self.url = url
            self.driver = webdriver.Chrome()

        def get_cookie(self):
            self.driver.get(self.url)
            time.sleep(2)
            cookies = self.driver.get_cookies()
            print(cookies)
            str_cookie = ''
            for j in cookies:
                name = j['name']
                value = j['value']
                str_cookie = str_cookie + name + '=' + value + ';'
            # 关闭浏览器
            self.driver.close()
            # 返回cookie
            print(str_cookie)
            return str_cookie


if __name__ == '__main__':
    url = 'https://www.realtor.com/realestateandhomes-search/Escambia-County_AL'
    c = Cookie(url)
    c.get_cookie()

