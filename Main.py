#coding:utf-8
from __future__ import with_statement # Required in 2.5
import signal
from urllib.request import urlopen
from bs4 import BeautifulSoup
from  pymongo import  MongoClient
import base64
from bs4 import  Tag
# from wechatsogou import  *
import requests
from  requests import RequestException
# from lxml import etree
from urllib.parse import urlparse
from gzhApi import GzhApi
import  json
import logging
import urllib
import itertools
from threading import  Thread
from BaiduHotwords import SearchByBaiduHotwords
from  gzhTor import SougouGzhTitleSearch
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  *
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import re
import time
import signal
import rstr
from contextlib import contextmanager
from pymongo import  MongoClient
import pymongo
from bson import Binary, Code
import bson.json_util
from wxsend import MyWXBot
logging.basicConfig(level = logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(filename='access.log',mode='w')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


# def getTitle(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         return  None
#     try:
#         bsObj = BeautifulSoup(html.read())
#         title = bsObj.body.h1
#         nameList = bsObj.findAll("span", {"class":"green"})
#         for name in nameList:
#             print(name.get_text())
#     except AttributeError as e:
#         return  None
#     return  title



# def weixinSpider():
#     wcApi = GzhApi()
#     text = wcApi.search_gzh_info("吴晓波频道")
#     try:
#         bsObj = BeautifulSoup(text)
#         gzhs = bsObj.find_all("div","wx-rb_v1")
#         gzhNumTag = bsObj.find('resnum')
#         if gzhNumTag:
#             gzhNum = gzhNumTag.get_text()
#             print(gzhNum)
#         if gzhs:
#             for gzh in gzhs:
#                 print("===============================================================")
#                 for child in gzh.children:
#                     if isinstance(child,Tag):
#                         className = child.attrs['class'][0]
#                         if className == 'img-box':
#                             img = child.find("img")
#                             avatarUrl = img.attrs['src']
#                         if className == 'txt-box':
#                             weixinaliasTag = child.find(attrs={'name':'em_weixinhao'})
#                             introduceTag = child.find('span','sp-txt')
#                             recentArticalTag = child.find('a')
#                             if weixinaliasTag:
#                                weixinalias =  weixinaliasTag.get_text()
#                             if introduceTag:
#                                 introduce = introduceTag.get_text()
#                                 print(introduce)
#                             if recentArticalTag:
#                                 articalUrl = recentArticalTag.attrs['href']
#                                 articalTitle = recentArticalTag.get_text()
#                                 articalDateTag = child.find('span','hui')
#                                 if articalDateTag:
#                                     articalDate = articalDateTag.get_text()[22:-2]
#                                 wcApi.openArticl(articalUrl)
#
#
#
#
#
#     except AttributeError as e:
#         return  None
#     pass

import os
import requests


url = 'https://api.ipify.org?format=json'


def getip_requests(url):
    print("(+) Sending request with plain requests...")
    r = requests.session().get(url)
    print("(+) IP is: " + r.text.replace("\n", ""))


def getip_requesocks(url):
    print("(+) Sending request with requesocks...")
    session = requests.session()
    proxies = {'http': 'socks5://127.0.0.1:9150',
                       'https': 'socks5://127.0.0.1:9150'}
    r = session.get(url,proxies= proxies)
    print("(+) IP is: " + r.text.replace("\n", ""))





"""
查看网站技术
"""


def download(url,num_retries=2):
    logging.debug('Downloading:',url)
    try:
        response = urllib.request.urlopen(url)
        html = response.read()
    except urllib.error.URLError as e:
        logging.debug('Download error:',e.reason)
        html = None
        if num_retries > 0 :
            if hasattr(e,'code') and 500 <= e.code < 600:
                return  download(url,num_retries-1)
    logging.debug(html)
    return  html

def excri():
    max_errors = 5
    num_errors = 0
    for page in itertools.count(1):
        url = "http://example.webscraping.com/view/-%d" % page
        html = download(url)
        if html is None:
            num_errors +=1
            if num_errors == max_errors:
                break
        else:
            num_errors = 0


class SougouMainPageSearchThread(Thread):
    def run(self):
        sougou =  SougouGzhTitleSearch()
        sougou.sougouMainPage()

class BaiduHotwordsThread(Thread):
    def run(self):
        articleSearch = SearchByBaiduHotwords()







# if __name__ == '__main__':
#     t =  SougouMainPageSearchThread()
#     a =  BaiduHotwordsThread()
#     t.setDaemon(True)
#     a.setDaemon(True)
#     a.start()
#     t.start()

    # daemon = Gzh("/var/run/gzh.pid")
    # daemon.start()
    # daemon.run()
    # if len(sys.argv) >= 2:
    #     if 'start' == sys.argv[1]:
    #         daemon.start()
    #     elif 'stop' == sys.argv[1]:
    #         daemon.stop()
    #     elif 'restart' == sys.argv[1]:
    #         daemon.restart()
    #     else:
    #         print("Unknown command")
    #         sys.exit(2)
    #     sys.exit(0)
    # else:
    #     print("usage: %s start|stop|restart" % sys.argv[0])
    #     sys.exit(2)

# import threading
# import datetime
#
# class ThreadClass(threading.Thread):
#     def run(self):
#        sougou =  SougouGzhTitleSearch()
#        sougou.sougouMainPage()
#
# class ThreadClass2(threading.Thread):
#     def run(self):
#
#         articleSearch = SearchByBaiduHotwords()
#
# t1 = ThreadClass()
# t1.start()
# t2 = ThreadClass2()
# t2.start()

# z=MjM5NzI4OTY0NQ==&scene=110&uin=MjI3MjE1NDYyMA%3D%3D&ke

# 9ed31d4918c154c8070a3caf09fc2354b43bab0185d6e1e0fb76e8ede8b6562fc22994dbd971762a674717306a272a97d659084a53484f9c37be9fc2c9402ce6424aa7036edc3809960606b0e2a8574f

# headers = {"Host":"mp.weixin.qq.com",
#            # "X-WECHAT-KEY":"9ed31d4918c154c8e69792937f7c1aeefb81ea1ae8e4fddb1d7028300eb424f0412705809af867d4b838d8c6a18394ee5a3d6a422cd89f0457c8b3a07cd7ae5e71c1c708e4408f731b45d92264f4b586",
#            # "X-WECHAT-UIN":"MjI3MjE1NDYyMA%3D%3D",
#            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#            # "Cookie":"wap_sid=CPynubsIEkAxSHoxcmQ5bG13aEZrRHhDOHNjSVFtWGkxTWJlckVCRFdLOFNxSUU4LU0tazJYVnI5YmdZbFZZbjFYc0pBdHFhGAQg/REo1tGI+AgwprmKwQU=;wxticket=4098806190; wxticketkey=9fe18175984f426cdaee4678c91ce623dc0326f316f81d4b1f64f769e3fab209;wxtokenkey=7c60ee7534b45e5f8943c5e38e0c867fdc0326f316f81d4b1f64f769e3fab209; pgv_pvid=2731283494;sd_cookie_crttime=1468299221723;sd_userid=14871468299221723",
#            "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.3.25 NetType/WIFI Language/zh_CN",
#            "Accept-Language":"zh-cn",
#            "Accept-Encoding":"gzip,deflate",
#            "Connection":"keep-alive"}
# cookies = {}
#
# firefox_capabilities = DesiredCapabilities.PHANTOMJS
# for key, value in enumerate(headers):
#     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
# firefox_capabilities['marionette'] = True
# driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
# driver.get("http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5NjM4NTAwMQ==&scene=110&uin=MjI3MjE1NDYyMA%3D%3D&key=9ed31d4918c154c8c9fb88eb7cb9c11b90b77b98c9c6a8cd98c5c5e9818f5fee3a4251e9b50b5e554c18db628b7cadd04f3fae68b63c42c8785b91a6f5802312ef3d25777861ecb6b875cffb0a9d344d")
# res = requests.session().get("https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5NjM4NTAwMQ==&scene=110&uin=MjI3MjE1NDYyMA%3D%3D&key=9ed31d4918c154c8070a3caf09fc2354b43bab0185d6e1e0fb76e8ede8b6562fc22994dbd971762a674717306a272a97d659084a53484f9c37be9fc2c9402ce6424aa7036edc3809960606b0e2a8574f",headers=headers)
# res.encoding = "utf-8"
# print(res.text)



# headers2 = {"Host":"mp.weixin.qq.com",
# "Accept":"*/*",
# "X-Requested-With":"XMLHttpRequest",
# "Accept-Encoding":"gzip, deflate",
# "Accept-Language":   "zh-cn",
# "Content-Type":      "application/x-www-form-urlencoded; charset=UTF-8",
# "Origin":            "https://mp.weixin.qq.com",
# "Content-Length":    "60",
# "Connection":        "keep-alive",
# "User-Agent":        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.3.25 NetType/WIFI Language/zh_CN",
# "Referer":           "https://mp.weixin.qq.com/s?__biz=MzA3OTM5NTkxNA==&mid=2652410357&idx=1&sn=ace3edc6b20bda30559b5c1fc176d9f5&chksm=84581cd0b32f95c6f3c1ca86c5502fef9ab0e22cf13df87dbe64901395814b0273159b2535a7&scene=0&key=194655c10e3d29b1128b115e11c7e4e838294de1f5e8e82f4f26b11389e0da6a727b9814e0da5f2f3b954197e892fae0&ascene=7&uin=MjI3MjE1NDYyMA%3D%3D&devicetype=iPhone+OS10.1.1&version=16031912&nettype=WIFI&fontScale=100&pass_ticket=%2BPKkTTyCMFrLGIj2YYriQ09tL%2ByP%2FgFXOVdV2UfoLg5ReIH3RK82qZ1kyNfV2j2x",
# "Cookie":            "wap_sid=CPynubsIEkBuMzFfMFhTMllRRm83YTJQZmx4S1ExYkRiQ3I3OXVMclJvZk1ScXhmYi1QaU9sdjN6OTZrYmtoWjViMVJ3Vy1TGAQg/BEoyrSvvAswheyKwQU=; wxticket=1535816442;wxticketkey=8051c5df478763bf49c3dbd1816fb798432c89a1309997d92edc48d6192b6669;wxtokenkey=2319ccd9edfc9a65941bc830585f657b432c89a1309997d92edc48d6192b6669; pgv_pvid=2731283494;sd_cookie_crttime=1468299221723; sd_userid=14871468299221723"
#             }
# payload = {'is_only_read': 1, 'req_id': '0913o4oIg5jSBAQCHBcUnfnX','is_temp_url:':0}
# res2 = requests.session().post("https://mp.weixin.qq.com/mp/getappmsgext?__biz=MzA3OTM5NTkxNA==&appmsg_type=9&mid=2652410357&sn=ace3edc6b20bda30559b5c1fc176d9f5&idx=1&scene=0&title=%E6%88%91%E4%BB%AC%E7%9A%84%E7%B2%89%E4%B8%9D%E7%A0%B4200%E4%B8%87%E4%BA%86%EF%BC%81&ct=1478646684&abtest_cookie=&devicetype=iPhone&nbsp;OS10.1.1&version=/mmbizwap/zh_CN/htmledition/js/appmsg/index31ab69.js&f=json&r=0.6455886808458782&is_need_ad=1&comment_id=3062142033&is_need_reward=0&both_ad=1&reward_uin_count=0&msg_daily_idx=1&uin=MjI3MjE1NDYyMA%253D%253D&key=194655c10e3d29b1128b115e11c7e4e838294de1f5e8e82f4f26b11389e0da6a727b9814e0da5f2f3b954197e892fae0&pass_ticket=%25252BPKkTTyCMFrLGIj2YYriQ09tL%25252ByP%25252FgFXOVdV2UfoLg5ReIH3RK82qZ1kyNfV2j2x&wxtoken=2012833448&devicetype=iPhone%26amp%3Bnbsp%3BOS10.1.1&clientversion=16031912&x5=0",data=payload,headers=headers2)
# res2.encoding = "utf-8"
# s = res2.text
# print(res2.text)

cookies_dict = {}

@contextmanager
def time_limit(seconds):
    def signal_handler(signum,frame):
        raise Exception("time out!")
    signal.signal(signal.SIGALRM,signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# def qqLogin():
#         firefox_capabilities = DesiredCapabilities.PHANTOMJS
#         firefox_capabilities['marionette'] = True
#         driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
#         driver.get("http://weixin.sogou.com")
#         wait = WebDriverWait(driver,2)
#         try:
#             wait.until(expected_conditions.visibility_of_element_located((By.ID,"loginBtn")))
#
#         except Exception as e:
#             logging.debug(e)
#         finally:
#             qqloginBtn = driver.find_element_by_id('loginBtn')
#             qqloginBtn.click()
#         try:
#             iframes = driver.find_element_by_tag_name('iframe')
#             driver.switch_to_frame(iframes)
#             driver.switch_to_frame('ptlogin_iframe')
#             uploginTag = driver.find_element_by_id('switcher_plogin')
#             uploginTag.click()
#             uTag = driver.find_element_by_id('u')
#             pTag = driver.find_element_by_id('p')
#             uTag.send_keys('79188094')
#             pTag.send_keys('223006652zsj')
#             driver.find_element_by_class_name("login_button").click()
#             driver.switch_to_default_content()
#             try:
#                 with time_limit(30):
#                  while True:
#                         cookies_list = driver.get_cookies()
#                         logined = False
#                         for cookie in cookies_list:
#                             if cookie['name'] == 'pprdig':
#                                 logined = True
#                                 break
#                         if logined:
#                             break;
#             except RuntimeError:
#                 logging.debug("time out")
#             # time.sleep(30)
#             # driver.get("http://weixin.sogou.com/weixin?query=习近平&_sug_type_=&_sug_=n&type=1&page=100")
#             # text = driver.page_source
#             cookies_list = driver.get_cookies()
#             global cookies_dict
#             for cookie in cookies_list:
#                cookies_dict[cookie['name']] = cookie['value']
#         except Exception as e:
#             logging.debug(e)
# qqLogin()
# sess = requests.session()
# res = sess.get("http://weixin.sogou.com/weixin?query=习近平&_sug_type_=&_sug_=n&type=1&page=100",cookies = cookies_dict)
# text = res.text
# print(text)


# client = MongoClient()
# db = client['gzh']
# records = db.gzhs.find({"biz":{"$exists": 1}})
# collection = db.gzhs

# for record in records:
#
#     if record["biz"][0] == "\"":
#         # biz = record["biz"][23:]
#         collection.remove({'wid':record["wid"]})
#     elif len(record["biz"]) != 16:
#         collection.remove({'wid':record["wid"]})
#     else:
#         biz = record["biz"]
#         # print(base64.b64decode(biz).decode("utf-8"))
# print("complete")
#M[a-z][A-Z][a-z0-9][A-Z][A-Za-z][A-Z][a-z0-9][A-Z][A-Za-z][A-Za-z][a-z0-9][A-Z][A-Za-z]==/g
# print(rstr.xeger(r'M[a-z][A-Z][a-z0-9][A-Z][A-Za-z][A-Z][a-z0-9][A-Z][A-Za-z][A-Za-z][a-z0-9][A-Z][A-Za-z]=='))

# print(base64.b64decode("MjM5NzI4OTY0NA==").decode("utf-8"))

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.key = None
        self.uin = None
        self.isrunning = False;
        self.gzhheaders = None;
        self.gzhcookies = None;
        self.gzhquery = None;
        client = MongoClient()
        db = client['gzh']
        records = db.gzhs.find({"biz":{"$exists": 1}})
        self.collection = db.gzh_pre
        self.collection.count(with_limit_and_skip=True)


    def get(self):
        # self.gzhheaders = self.get_query_argument("a")
        # self.gzhcookies = self.get_query_argument("b")
        # self.gzhquery = self.get_query_argument("c")
        # if self.isrunning == False:
        #     self.queryGzh()
        pass

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        self.gzhheaders = data['headers']
        self.gzhcookies = data['cookies'];
        self.gzhquery = data['query']
        self.write("ok")
        if self.isrunning == False:
            self.queryGzh()


    def queryGzh(self):
        # if self.key != None and self.uin != None:
            self.isrunning = True
            startIndex = 2399454465
            endIndex = 3200125886
            record = self.collection.find_one({},sort=[('_id',pymongo.DESCENDING)]);
            if record != None :
                startBiz = record['biz']
                startIndex = int(base64.b64decode(startBiz).decode("utf-8"))+1
            proxies = {
                "http": "http://117.33.201.53:8998",
                "https": "https://117.33.201.53:8998",
            }
            # for i in range(2399454465,3200125886):

                # headers = json.loads(self.gzhheaders)
                # cookies = json.loads(self.gzhcookies)
                # biz = base64.b64encode(str(i).encode("utf-8")).decode('utf-8')
            url = "https://mp.weixin.qq.com/mp/getmasssendmsg?__biz="+self.gzhquery['__biz']
            # url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz="+self.gzhquery['__biz'];
            for k,v in self.gzhquery.items():
                if k == 'uin' or k == 'key' :
                    url = url+"&"+k+"="+v

            firefox_capabilities = DesiredCapabilities.PHANTOMJS
            for key, value in enumerate(self.gzhheaders):
                webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
            firefox_capabilities['marionette'] = True
            driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
            driver.get(url)
                # session = requests.session()
                # res = session.get(url,headers=self.gzhheaders,cookies = self.gzhcookies)
                # res.encoding = "utf-8"
                # text = res.text
                # print(text)
                # self.collection.insert_one({'biz':biz,'oritext':text});
                # time.sleep(10)

bot = None
class SendGzhHandler(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient()
        db = client['gzh']
        collection = db.gzhs
        records = list(collection.find({"biz":{"$exists": 1}}).limit(20))
        result = bson.json_util.dumps(records)
        self.write(result)

    def post(self):
        pass

class SendingGzhHandler(tornado.web.RequestHandler):

    def get(self):
        client = MongoClient()
        db = client['gzh']
        collection = db.gzhs
        records = list(collection.find({"biz":{"$exists": 1}}).limit(20))
        record = records[0];
        biz = record['biz'];
        url = "http://mp.weixin.qq.com/mp/profile_ext?action=home&__biz="+biz+"&scene=110#wechat_redirect";
        print(url)
        if bot != None and bot.logined:
            bot.send2Filehelper(url);
            pass

    def post(self):
        pass


class HandingGzhUrlHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.key = None
        self.uin = None
        self.isrunning = False;
        self.gzhheaders = None;
        self.gzhcookies = None;
        self.gzhquery = None;

    def get(self):
        pass

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        self.gzhheaders = data['headers']
        self.gzhcookies = data['cookies'];
        self.gzhquery = data['query']
        self.queryGzh()

    def queryGzh(self):
        # if self.key != None and self.uin != None:
            self.isrunning = True
            # for i in range(2399454465,3200125886):

                # headers = json.loads(self.gzhheaders)
                # cookies = json.loads(self.gzhcookies)
                # biz = base64.b64encode(str(i).encode("utf-8")).decode('utf-8')
            url = "https://mp.weixin.qq.com/mp/getmasssendmsg?__biz="+self.gzhquery['__biz']
            # url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz="+self.gzhquery['__biz'];
            for k,v in self.gzhquery.items():
                if k == 'uin' or k == 'key' :
                    url = url+"&"+k+"="+v
            firefox_capabilities = DesiredCapabilities.PHANTOMJS
            for key, value in enumerate(self.gzhheaders):
                webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
            firefox_capabilities['marionette'] = True
            driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
            driver.get(url)
def make_app():
    return tornado.web.Application([
        (r"/gzh/getSendingGzh", SendGzhHandler),
        (r"/gzh/sendingGzh", SendingGzhHandler),
        (r"/gzh/handingGzhUrl", HandingGzhUrlHandler),
    ])
def startWx():
    global bot
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()
if __name__ == "__main__":
    t = Thread(target=startWx)
    t.start()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

    # if bot.logined:






