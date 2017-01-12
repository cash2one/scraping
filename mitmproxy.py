from mitmproxy import ctx
import requests
from requests_futures.sessions import FuturesSession
import json
def request(flow):

    if len(flow.request.path_components) == 1:
        path = flow.request.path_components[0]
        if path == 's':
            key = flow.request.query['key']
            uin = flow.request.query['uin']
            if key and uin:
                headers = {}
                cookies = {}
                query={}
                for k, v in flow.request.cookies.items():
                    # print(k+"="+ v)
                    cookies[k]=v
                for k, v in flow.request.query.items():
                    # print(k+"="+ v)
                    query[k]=v
                for k, v in flow.request.headers.items():
                    # print(k+"="+ v)
                    headers[k]=v
                a = json.dumps(headers)
                b = json.dumps(cookies)
                c = json.dumps(query)
                data = {}
                data['headers'] = headers
                data['cookies'] = cookies
                data['query'] = query
                session = FuturesSession()
                future = session.post("http://127.0.0.1:8888/gzh/handingGzhUrl",data=json.dumps(data))
                ctx.log.error("key= "+key+" uin="+uin)

def start():
    ctx.log.info("This is some informative text.")
    ctx.log.error("This is an error.")