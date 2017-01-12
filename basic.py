
import requests
import  random
from exceptions import  *
class WechatSearchBasic(object):
    def __init__(self,**kwargs):
        self.session = requests.session()
        self._agent = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
        ]


    def _get(self,url,rtype='get',**kwargs):
        """
        封装get post方法
        :param url:
        :param rtype:
        :param kwargs:
        :return:
        """
        proxies = {
            # "http":"socks5://127.0.0.1:9150",
    }
        referer = kwargs.get('referer',None)
        host = kwargs.get('host', None)
        if host:
            del kwargs['host']
        if referer:
            del  kwargs['referer']
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
            "Referer": referer if referer else 'http://weixin.sogou.com/',
            'Host': host if host else 'weixin.sogou.com',
            'Accept-Charset': 'utf-8'
        }
        if rtype == 'get':
            r = self.session.get(url,headers = headers,proxies= proxies,**kwargs )
        else:
            data = kwargs.get('data', None)
            json = kwargs.get('json', None)
            r = self._session.post(url, data=data, json=json, headers=headers,proxies= proxies, **kwargs)
        if r.status_code == requests.codes.ok:
            r.encoding = self._get_encoding_from_reponse(r)
            if u'用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in r.text:
                self._vcode_url = url
                raise WechatSogouVcodeException('weixin.sogou.com verification code')
        else:
            raise Exception('requests status_code error', r.status_code)
        return r.text

    def _get_encoding_from_reponse(self, r):
        """获取requests库get或post返回的对象编码

        Args:
            r: requests库get或post返回的对象

        Returns:
            对象编码
        """
        encoding = requests.utils.get_encodings_from_content(r.text)
        return encoding[0] if encoding else requests.utils.get_encoding_from_headers(r.headers)