#coding:utf-8
import signal
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
from contextlib import contextmanager
logging.basicConfig(level = logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileHandler = logging.FileHandler(filename='access.log',mode='w')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)
"""
定时任务
"""
# def calcProd():
#     product = 1
#     for i in range(1,100000):
#         product = product + i
#     return product
# startTime = time.time()
# prod = calcProd()
# endTime = time.time()
# logging.debug('The result is %s digits long' % (len(str(prod))))
# logging.debug('Took %s seconds to calculate' % (endTime - startTime))

"""
多线程
"""
# logging.debug('Start of program.')
# def takeANap():
#     time.sleep(5)
#     logging.debug('Wake up!')
# threadObj = threading.Thread(target=takeANap)
# threadObj.start()
# logging.debug('End of program.')

"""
多线程传递参数
"""
# threadObj = threading.Thread(target=logging.debug,args=['Cats','Dogs','Frogs'],kwargs={'sep':'&'})
# threadObj.start()
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
class SearchGzhByArticalKeywords:
    def __init__(self,articalKeywords):
        self.api = GzhApi()
        self.driver = None
        self.cookies_dict = {}
        self.getSougouDriver()



    def sougouPage(self,totalItemStr):
        totalItem = 0
        if ',' in totalItemStr:
            totalItemStr = totalItemStr.replace(',','')
            logging.debug(totalItemStr)
        try:
            p = re.compile(r"[1-9]\d+")
            m = p.match(totalItemStr)
            if m != None:
                totalItem = int(m.group())
        except:
            logging.debug("总页数不是数字")
        if totalItem % 10 == 0:
                page = totalItem/10
        else:
                page = int(totalItem/10) + 1
        return page

    def startSpide(self,articalKeywords):
        self.articalKeywords = articalKeywords ;
        # hotwords = self.getBaiduHotword()
        # for title in hotwords:
        self.searchArtical(self.articalKeywords)
    def getSougouDriver(self):
        firefox_capabilities = DesiredCapabilities.PHANTOMJS
        firefox_capabilities['marionette'] = True
        # self.driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromeDriver")
        self.qqLogin()

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
        self.getPage("http://weixin.sogou.com")
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
            die_after = time.time()+80
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

    def searchArtical(self,keyword):
        # upqueryTag = self.driver.find_element_by_id('upquery')
        # upqueryTag.send_keys(keyword)
        # articalBtn = self.driver.find_element_by_class_name('swz')
        # articalBtn.click()
        self.newfindGzhTitle(keyword)

    def newfindGzhTitle(self,keyword):
        currentArticalPage = 0
        totalArticalPage = 0
        while True:
            currentArticalPage+=1
            request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
                keyword) + '&_sug_type_=&_sug_=n&type=2&page=' + str(currentArticalPage) + '&ie=utf8'
            pageSource = self.requestPage(request_url)
            soup = bs4.BeautifulSoup(pageSource)
            if currentArticalPage == 1:
                #获得总页数
                totalNumTag =  soup.select(".mun")
                #说明不够一页
                if totalNumTag is None or len(totalNumTag) == 0:
                    totalArticalPage = 1
                else:
                    totalArticalPageStr = totalNumTag[0].get_text()
                    totalArticalPage = self.sougouPage(totalArticalPageStr)
            #解析获得每个页面的公众号title
            boxs =  soup.select(".account")
            if boxs is None:
                logging.debug("没有找到公众号名字")
            for boxTag in boxs:
                gzhTitle = boxTag.get_text()
                self.newfindGzhByTitle(gzhTitle)
            if currentArticalPage == totalArticalPage:
                break;
            if currentArticalPage == 100:
                break;
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
    def getGzhBiz(self,url):
        request_url = url
        api = GzhApi();
        # soup = bs4.BeautifulSoup(self.driver.page_source)
        time.sleep(10)
        text = api.openWeixinPage(request_url)
        p = re.compile(r"\bvar\s*biz\s*=\s*\"\w+==\"")
        m = p.search(text)
        if m != None:
            bizStr = m.group()
            biz = bizStr[11:len(bizStr)-1]
            logging.debug(biz)
            return biz;
        logging.debug("没有找到biz")
        return None

    def newfindGzhByTitle(self,title):
        try:
            client = MongoClient()
            db = client['gzh']
            currentArticalPage = 0
            totalArticalPage = 0
            while True:
                currentArticalPage+=1
                request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
                    title) + '&_sug_type_=&_sug_=n&type=1&page=' + str(currentArticalPage) + '&ie=utf8'
                page_source = self.requestPage(request_url)
                #获得公众号信息
                soup = bs4.BeautifulSoup(page_source)
                if currentArticalPage == 1:
                    #获得总页数
                    totalArticalPageTag = soup.select(".mun")
                    #说明不够一页
                    if totalArticalPageTag is None or len(totalArticalPageTag) == 0:
                        totalArticalPage = 1
                    else:
                        totalArticalPageStr = totalArticalPageTag[0].get_text()
                        totalArticalPage = self.sougouPage(totalArticalPageStr)
                # gzhTitleTags = soup.select('.txt-box .tit')
                gzhIDTags = []
                gzhInstrucationTags = []
                gzhAuthenticationTags = []
                gzhTitles= []
                gzhs = []
                tags =  soup.select('.news-box li')
                for i in range(len(tags)):
                    boxTag =  tags[i]
                    weixinIDTag = boxTag.find('label',{'name':'em_weixinhao'})
                    weixinID = weixinIDTag.get_text()
                    gzhIDTags.append(weixinID)
                    weixinTitleTag = boxTag.select('.txt-box a')
                    weixinUrl = None
                    if weixinTitleTag is None:
                        weixinTitle = ''
                    else:
                        weixinTitle = weixinTitleTag[0].get_text()
                        weixinUrl = weixinTitleTag[0]['href']
                    gzhTitles.append(weixinTitle)
                    dlTags = boxTag.select("dl")
                    functionTextTag = dlTags[0]
                    functionText = ''
                    if functionTextTag != None:
                        functionText = functionTextTag.get_text()
                    gzhAuthenticationText = ''
                    try:
                        gzhAuthenticationTag = dlTags[1]
                    except:
                        gzhAuthenticationTag= None
                    if gzhAuthenticationTag != None:
                        gzhAuthenticationText = gzhAuthenticationTag.get_text()
                    gzhInstrucationTags.append(functionText)
                    gzhAuthenticationTags.append(gzhAuthenticationText)
                # for ids in range(len(gzhIDTags)):
                    content = {}
                    content['wid'] = weixinID
                    content['tip'] = functionText
                    content['authentication'] = gzhAuthenticationText
                    content['title'] = weixinTitle
                    biz = self.getGzhBiz(weixinUrl)
                    content['biz'] = '' if biz == None else biz
                    gzhs.append(content)
                if len(gzhs)>0 :
                    result  = db.gzhs.insert_many(gzhs)
                    logging.debug("保存数据")

                if currentArticalPage == totalArticalPage:
                    break;
                if currentArticalPage == 100:
                    break
        except Exception as e:
                print(e)


