#coding:utf-8
import  random
import types
import webbrowser
import requests,bs4,os
import logging
from selenium import webdriver
import sys
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  *
from  selenium.webdriver.common.keys import Keys
import threading
from urllib.request import quote as quote
import builtwith
from gzhApi import GzhApi
import itertools
import urllib.request
import urllib.error
from  pymongo import  MongoClient
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import json
from urllib.parse import urlparse,parse_qsl
from SearchGzhByArticalKeywords import SearchGzhByArticalKeywords
from contextlib import contextmanager
import signal
logging.basicConfig(level = logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileHandler = logging.FileHandler(filename='access.log',mode='w')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

driver = None
mainPage = None

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
class SougouGzhTitleSearch:
    def __init__(self):
        self.cookies_dict = {}
        self.getSougouDriver()
        self.api = GzhApi()


    def waitAntiSpider(self,waitSeconds=3):
        urlParseRes = urlparse(self.driver.current_url)
        wait = True ;
        if urlParseRes is not  None:
                path = urlParseRes[2]
                if 'antispider' in path:
                    request_url = parse_qsl(urlParseRes.query)[0][1]
                    self.driver.quit()
                    logging.debug("有验证码 退出")
                    time.sleep(waitSeconds)
                    self.getSougouDriver()
                    logging.debug("避开验证码 开始"+"http://weixin.sogou.com"+request_url)
                    # self.requestPage("http://weixin.sogou.com"+request_url)
                    waitSeconds+=1
                    return  self.waitAntiSpider(waitSeconds)
                    # soup = bs4.BeautifulSoup(self.driver.page_source)
        return wait

    def getPage(self,page):
        self.antiWaitSeconds = 3
        try:
            self.driver.get(url=page)
            self.waitAntiSpider(self.antiWaitSeconds);
        except TimeoutException as e:
            logging.debug("time out 等待重试")
            time.sleep(30)
            self.getPage(page)

    def requestPage(self,page):
        return self.api.openSogouPage(page,self.cookies_dict)


    def qqLogin(self):
        wait = WebDriverWait(self.driver,2)
        try:
            wait.until(expected_conditions.visibility_of_element_located((By.ID,"loginBtn")))

        except Exception as e:
            logging.debug(e)
        finally:
            qqloginBtn = self.driver.find_element_by_id('loginBtn')
            qqloginBtn.click()
        try:
            wait.until(expected_conditions.visibility_of_element_located((By.ID,"iframe")))
        except Exception as e:
            logging.debug(e)
        finally:
            iframes = self.driver.find_element_by_tag_name('iframe')
            self.driver.switch_to_frame(iframes)
        try:
            wait.until(expected_conditions.visibility_of_element_located(By.ID,"ptlogin_iframe"))
        except Exception as e:
            logging.debug(e)
        finally:
            self.driver.switch_to_frame('ptlogin_iframe')
        try:
             wait.until(expected_conditions.visibility_of_element_located(By.ID,"switcher_plogin"))
        except Exception as e:
            logging.debug(e)
        finally:
            uploginTag = self.driver.find_element_by_id('switcher_plogin')
            uploginTag.click()
            uTag = self.driver.find_element_by_id('u')
            pTag = self.driver.find_element_by_id('p')
            uTag.send_keys('79188094')
            pTag.send_keys('223006652zsj')
            self.driver.find_element_by_class_name("login_button").click()
            self.driver.switch_to_default_content()
            die_after = time.time()+30
            while True:
                cookies_list = self.driver.get_cookies()
                logined = False
                for cookie in cookies_list:
                    if cookie['name'] == 'pprdig':
                        logined = True
                        break
                if logined:
                    break;
                if time.time() > die_after:
                    logging.debug("time out")
                    break;
            for cookie in cookies_list:
               self.cookies_dict[cookie['name']] = cookie['value']
    def getSougouDriver(self):
        firefox_capabilities = DesiredCapabilities.PHANTOMJS
        firefox_capabilities['marionette'] = True
        self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        self.getPage("http://weixin.sogou.com")
        self.mainPage = bs4.BeautifulSoup(self.driver.page_source)
        self.qqLogin()

    def updateBiz(self):
        client = MongoClient()
        db = client['gzh']
        collection = db.gzhs
        search = SearchGzhByArticalKeywords("")
        for gzh in collection.find():
            wid = gzh['wid']
            biz = search.getGzhBiz(wid)
            if biz != None:
                result = collection.update_one({'wid':wid},{'$set': {'biz': biz}})
                logging.debug("wid = "+wid+" biz = "+biz)
            logging.debug("wid = "+wid+" biz is None")


    def sougouMainPage(self):
        titles =[]
        articles = []
        articles = titles +self.getTopNews()
        articles = titles +self.getTopWords()
        titles = titles +self.getRecommend()
        titles = titles +self.getHotCollection()
        search = SearchGzhByArticalKeywords()
        for article in articles:
            search.startSpide()
        for keyword in titles:
            search.newfindGzhByTitle(keyword)
    def getTopNews(self):
        topTags = self.mainPage.find_all('div',{'class':'wx-news'})
        titles = []
        for tag in topTags:
            a = tag.find('a')
            title = a.get_text()
            titles.append(title)
        return titles;


    def getTopWords(self):
        hotwords = self.mainPage.find_all('div',{'class':'wx-ph'})
        titles = []
        for hotword in hotwords:
            if hotword != None:
                links = hotword.find_all('a')
                for link in links:
                    title = link.get_text()
                    titles.append(title)
        return titles

    def getRecommend(self):
        linkTags = self.mainPage.find_all('div',{'class':'wx-tabbox2'})
        recommendTypeCount =  len(linkTags)
        titles = []
        for i in range(recommendTypeCount):
            requestUrl = "http://weixin.sogou.com/pcindex/pc/pc_"
            index = 0 ;
            while True:
                #从1开始
                index+=1
                if index == 1:
                    requestUrl = "http://weixin.sogou.com/pcindex/pc/pc_"+str(i)+"/pc_"+str(i)+".html"
                else:
                    requestUrl = "http://weixin.sogou.com/pcindex/pc/pc_"+str(i)+"/"+str(index)+".html"
                try:
                    response = requests.session().get(requestUrl)
                    response.raise_for_status()
                    response.encoding = 'utf-8'
                    html = response.text
                except Exception as e:
                    break;
                # text = response.content.decode('utf-8')
                # text = html.encode(response.encoding).decode('utf-8')
                bsPage = bs4.BeautifulSoup(html);
                ps = bsPage.find_all('p')
                for p in ps:
                    if p.has_attr('title'):
                        title = p.get_text()
                        titles.append(title)
                if len(linkTags)<20:
                    break ;
        return titles;

    def getHotCollection(self):
        ulTags = self.mainPage.find_all('ul',{'class':'sc_news'})
        uTitles = []
        for uTag in ulTags:
            titles = uTag.find_all('p',{'class':'time'})
            for title in titles:
                title = title.find('a').get_text()
                uTitles.append(title)
        return uTitles


