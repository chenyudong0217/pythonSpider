#encoding: utf-8
import sys, os
import requests,json
import queue,time,threading
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.settings import proxy_url,ua_list

proxy_queue = queue.Queue()
info_task_queue = queue.Queue()

cookie = 'ASP.NET_SessionId=punkrywageuuigeyoijiltse; showUpdate=2023-11-27; Hm_lvt_a317640b4aeca83b20c90d410335b70f=1701828563; clx=y; sid=punkrywageuuigeyoijiltse; lawapp_web=C95A7DD2EA06043A683DA9638637D5FC0F83E52822C388EABB3FFBC95A7F8AA997CAF967CF61916DC1396A496D546F2B93C686E95E8A884E9F0F73241EA5EC89667EAE744866B12E720AD2D786A3CC4744EA5B211124C7D8F7FDBD752562D89861DBE654F1E3DA793EC1728096EE318214A0AB4A24341BE4B5B0BCCC4902DCBA25016BD980C80634621D42219E75F192D42572CC5A4B4076E543668AF5034EC6DA1D62FD; is_clx_timeout=1; is_show_user_timeout=1; insert_cookie=37836164; Hm_lpvt_a317640b4aeca83b20c90d410335b70f=1701841224'

def getProxy():
    print('开始申请获取代理ip')
    url = proxy_url
    while 1:
        try:
            while proxy_queue.qsize()>10:
                proxy_queue.get()
            response = requests.request("GET", url, headers={}, data={})
            content = response.text
            proxyConfig = json.loads(content)
            if (proxyConfig['status_code'] == 0):
                proxies = proxyConfig['proxies']
                for i in proxies:
                    if i['name'] == 'vps':
                        ips = i['proxyInfo']
                        for ip in ips:
                            if ip['interval'] >= 300:
                                continue
                            proxy_queue.put(ip)
            time.sleep(10)
        except Exception as e:
            print(e)

    print('退出代理ip获取逻辑')

def download(url):
    try:

    except Exception as e:
        print(e)
def spider_info():
    while 1:
        try:
            if info_task_queue.qsize() <= 0:
                time.sleep(2)
                continue
            url = info_task_queue.get()
            if url == None:
                time.sleep(2)
                continue
            download(url)
            time.sleep(0.5)
        except Exception as e:
            print(e)

def start_spider():
    for id in range(0,340769):
        print('A'+str(id))
        url = 'https://www.faxin.cn/lib/zyfl/ZyflContent.aspx?gid=A'+str(id)
        while info_task_queue.qsize() >= 100:
            time.sleep(2)
        info_task_queue.put(url)

if __name__ == '__main__':
    '''通过枚举遍历法条id方式测试法信试用会员账号单次访问上限'''
    print('法信详情页枚举遍历采集上限测试')
    #启动代理获取
    threading.Thread(target=getProxy).start()
    #启动多线程读取队列开始下载


    start_spider()