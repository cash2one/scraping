import requests
import json
from SearchGzhByArticalKeywords import SearchGzhByArticalKeywords
from threading import Thread
from multiprocessing import Process, Pool
import time





class SearchByBaiduHotwords:

    def __init__(self):
        hotwords = self.getBaiduHotword()
        search = SearchGzhByArticalKeywords(hotwords)
        for hotword in hotwords:
            search.startSpide(hotword)

    def getBaiduHotword(self):
        types = [0,1,2,3,4,5,6,8,10,14,15]
        hotwords = []
        i = 0;
        for i  in types:
            request_url ="http://news.baidu.com/n?m=rddata&v=hot_word&type="+str(i)+"&date="
            s = requests.session()
            s.keep_alive = False
            headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'news.baidu.com',
            'Upgrade-Insecure-Requests':'1'
        }
            r = s.get(request_url,headers=headers)
            i+=1
            time.sleep(1)
            if r.status_code == requests.codes.ok:
                data = json.loads(r.text)
                titles = data['data']
                for title in titles:
                    hotwords.append(title['title'])
        return hotwords

    def updateBiz(self):

        pass

