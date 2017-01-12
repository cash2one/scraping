try:
    from urllib.request import quote as quote
except ImportError:
    from urllib import quote as quote
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
from basic import WechatSearchBasic
from bs4 import BeautifulSoup
from bs4 import  Tag
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from exceptions import  *
from PIL import Image
import time
import  random
import re
import requests
try:
    import StringIO
    def readimg(content):
        return Image.open(StringIO.StringIO(content))
except ImportError:
    import tempfile
    def readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)
class GzhApi(WechatSearchBasic):
    def __init__(self,**kwargs):
        super(GzhApi,self).__init__(**kwargs)
        self.curProxy = None
    def search_gzh_info(self,name,page=1):
        """
        搜索公众号
        :param name: 搜索关键字
        :param page:搜索的页数
        :return:返回的文本
        """
        request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
            name) + '&_sug_type_=&_sug_=n&type=1&page=' + str(page) + '&ie=utf8'
        text = self._get(request_url)
        return text
    def openArticl(self,url):
        """

        :param 文章链接:
        :return:
        """
        text = self._get(url)
        bsObj = BeautifulSoup(text)
        readNumTag = bsObj.find(id='sg_readNum3')
        if readNumTag:
            readNum = readNumTag.get_text();
            print("阅读数="+readNum)

    def searchArtialByWord(self,keyword,page):
        request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
            keyword) + '&_sug_type_=&_sug_=n&type=2&page=' + str(page) + '&ie=utf8'
        try:
            text = self._get(request_url)
            # broswer = webdriver.Chrome(executable_path = '/Users/zhangshijie/bin/chromedriver');
            # broswer.get(request_url)
        except WechatSogouVcodeException as e:
            self._jiefeng()
            text = self._get(request_url, 'get', host='',
                             referer='http://weixin.sogou.com/antispider/?from=%2f' + quote(
                                 self._vcode_url.replace('http://', '')))
        return text,page

    def getWeiXinPage(self,url):
        text = self._get(url,rtype='get',host='mp.weixin.qq.com',referer='http://mp.weixin.qq.com')
        return  text

    def searchGzh(self,title,page=1):
        """
        搜索公众号
        :param name: 搜索关键字
        :param page:搜索的页数
        :return:返回的文本
        """
        try:
            request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
            title) + '&_sug_type_=&_sug_=n&type=1&page=' + str(page) + '&ie=utf8'
            text = self._get(request_url)
        except WechatSogouVcodeException as e:
            self._jiefeng()
            text = self._get(request_url, 'get', host='',
                             referer='http://weixin.sogou.com/antispider/?from=%2f' + quote(
                                 self._vcode_url.replace('http://', '')))

        return page, text
    def _jiefeng(self):
        """对于出现验证码，识别验证码，解封

        Args:
            ruokuai: 是否采用若快打码平台

        Raises:
            WechatSogouVcodeException: 解封失败，可能验证码识别失败
        """
        codeurl = 'http://weixin.sogou.com/antispider/util/seccode.php?tc=' + str(time.time())[0:10]
        coder = self._get(codeurl)
        # if hasattr(self, '_ocr'):
        #     result = self._ocr.create(coder.content, 3060)
        #     img_code = result['Result']
        # else:
        im = readimg(coder.content)
        im.show()
        img_code = input("please input code: ")
        post_url = 'http://weixin.sogou.com/antispider/thank.php'
        post_data = {
            'c': img_code,
            'r': quote(self._vcode_url),
            'v': 5
        }
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + quote(
                self._vcode_url.replace('http://', ''))
        }
        rr = self._session.post(post_url, post_data, headers=headers)
        remsg = eval(rr.content)
        if remsg['code'] != 0:
            raise WechatSogouVcodeException('cannot jiefeng because ' + remsg['msg'])
        # self._cache.set(config.cache_session_name, self._session)
        print('ocr ', remsg['msg'])

    def readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)

    def qqLogin(self):
        service_args = [
            '--proxy=127.0.0.1:1080',
            '--proxy-type=socks5',
        ]
        browser = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs',service_args=service_args)
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            ':Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'
        )
        dcap["browserName"] = (
            'chrome'
        )
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'weixin.sogou.com',
            'Upgrade-Insecure-Requests':'1'
        }
        for key,value in headers.items():
            DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        browser.get("http://weixin.sogou.com/")
        # browser.get('http://httpbin.org/headers')
        # cap_dict = browser.desired_capabilities
        # for key in cap_dict:
        #     print('%s: %s' % (key, cap_dict[key]))
        loginBtn = browser.find_element_by_id('loginBtn')
        loginBtn.click()
        browser.switch_to_frame('ptlogin_iframe')
        browser.find_element_by_id('switcher_plogin').click()
        uinput = browser.find_element_by_id('u')
        print(uinput)

    def openWeixinPage(self,page):
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
        }

        rr = self.session.get(page, headers=headers)
        # p = re.compile("验证码")
        # m = p.search(rr.text)
        # if m != None:
        #     rr = self.session.get(page, headers=headers,proxies = self.nextProxy())
        return rr.text
    def openSogouPage(self,page,cookies):
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
        }
        res = requests.session().get(page,cookies=cookies,headers = headers)
        return  res.text

    def nextProxy(self):
        proxies = [{"http":"http://35.154.8.210:80"},
                   {"http":"http://111.1.3.34:8000"},
                   {"http":"http://103.214.173.20:8080"},
                   {"http":"http://117.93.186.175:808"},
                   {"http":"http://171.37.171.3:8123"},
                   {"http":"http://113.139.1.169:8998"},
                   {"http":"http://120.52.73.98:8099"},
                   {"http":"http://222.91.175.175:8998"}]
        if self.curProxy is None:
            self.curProxy = proxies[0]
            return proxies[0]
        index = proxies.index(self.curProxy)
        index = index+1
        if index >= len(proxies):
            index = 0 ;
        self.curProxy = proxies[index]
        return self.curProxy