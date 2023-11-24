# encoding:utf-8
import sys, os
import time
import requests
from bs4 import BeautifulSoup
import queue, json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config.settings import proxy_url
import cookie as cookie_service
import db_func

proxy_queue = queue.Queue()
info_task_queue = queue.Queue()
list_task_queue = queue.Queue()


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
                            proxy_queue.put(ip)
            time.sleep(10)
        except Exception as e:
            print(e)

    print('退出代理ip获取逻辑')

#解析www站 法条详情页信息
def parse_info(content):
    info = {}
    soup = BeautifulSoup(content, 'html.parser')
    ##title
    title_node = soup.find('h2',attrs={'class':'title'})
    title = title_node.text.strip()
    info['title'] = title
    fields_nodes = soup.find('div',attrs={'class':'fields'}).find_all('li')
    for field_node in fields_nodes:
        field_str = field_node.text.strip()
        if field_str.__contains__('制定机关：'):
            issueDepartment = field_str.replace('制定机关：','').strip()
            info['issueDepartment'] = issueDepartment
        if field_str.__contains__('公布日期：'):
            issueDate = field_str.replace('公布日期：','').strip()
            info['issueDate'] = issueDate
        if field_str.__contains__('施行日期：'):
            implementDate = field_str.replace('施行日期：','').strip()
            info['implementDate'] = implementDate
        if field_str.__contains__('时效性：'):
            timelinessDic = field_str.replace('时效性：','').strip()
            info['timelinessDic'] = timelinessDic
        if field_str.__contains__('效力位阶：'):
            effectivenessDic = field_str.replace('效力位阶：','').strip()
            info['effectivenessDic'] = effectivenessDic
        if field_str.__contains__('法规类别：'):
            category = field_str.replace('法规类别：','').strip()
            info['category'] = category
    ##fullText
    fullText_node = soup.find('div',attrs={'id':'divFullText'})
    content = fullText_node.text.strip()
    info['content'] = content
    return info

## 存储提取的law_id入库，如果需要翻页将翻页params,或者失败重试 丢入任务队列
#返回任务是否结束
def parse_m_list(task, content, cookie):
    endPage = True
    try:
        params = task['params']
        result = json.loads(content)
        if result['code'] != 200 :
            if result['code'] == 401:
                '''token时效,触发account重新登录，cookie重新加载'''
                cookie_service.release_cookie()
            list_task_queue.put(task) ##重试请求失败的任务
            return False

        data = result['data']
        thisPage = data['page']
        totalPge = data['totalPage']
        if totalPge > thisPage and thisPage <= 50: #判断是否符合下翻页条件
            '''当前页小于最大页数，且小于等于50 表示还是继续下翻页'''
            params['page'] = thisPage+1
            task['params'] = params
            list_task_queue.put(task) #下发下翻页任务
            endPage = False
        '''开始列表解析'''
        for law in data['info']:
            db_func.add_law_id(law['gid'],law['title'],law['topicId'],law['columnId'])
    except Exception as e:
        print(e)
        endPage = False
    return endPage


#下载www站 法条详情页html
def download_info(url ,cookie):
    payload = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': cookie['www_cookie'],
        'Host': 'www.pkulaw.com',
        'Referer': 'https://www.pkulaw.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    try:
        proxyIp = proxy_queue.get()
        outDateTs = proxyIp['outDateTs']
        while int(time.time()) > outDateTs:
            proxyIp = proxy_queue.get()
            outDateTs = proxyIp['outDateTs']
        proxy = {'http':str(proxyIp['address']),'https':str(proxyIp['address'])}
        response = requests.request('GET', url, timeout=(10,10), headers=headers, data=payload, proxies=proxy)
        return response.text
    except Exception as e:
        print(e)




def download_law_list(task,cookie):
    try:
        url = 'https://m.pkulaw.com/api/mobile-server/platform-fabao/6.0.0.0.0/search/first'
        payload = json.dumps(json.loads(task['params']))
        headers = {
            'Host': 'm.pkulaw.com',
            'Content-Length': str(len(task['params'])),
            'Authorization': 'Bearer '+cookie['m_cookie'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Referer': 'https://m.pkulaw.com/',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        proxyIp = proxy_queue.get()
        outDateTs = proxyIp['outDateTs']
        while int(time.time()) > outDateTs:
            proxyIp = proxy_queue.get()
            outDateTs = proxyIp['outDateTs']
        proxy = {'http':str(proxyIp['address']),'https':str(proxyIp['address'])}
        response = requests.request("POST",url,headers=headers, data=payload,timeout=(10,10),proxies=proxy)
        if response.status_code == 401 or response.status_code == 567:
            list_task_queue.put(task)
            ##更新释放cookie
            cookie_service.release_cookie(cookie)
        return response.text
    except Exception as e:
        print(e)

# 从db中获取需要采集的list_params条件
def spider_law_id():
    print('spider law_list for law id')
    while 1:
        try:
            ##空值调出频次，避免下游堵塞任务无脑调出撑爆内存队列
            if list_task_queue.qsize() > 50:
                time.sleep(2)
                continue
            result = db_func.find_list_params()
            list_task_queue.put(result)
            db_func.update_list_task(result['id'],1)
            time.sleep(0.1)
        except Exception as e:
            print(e)

#下载执行器，开多个并发执行
def downloader():
    while 1:
        try:
            task = None
            if info_task_queue.qsize()>0:
                task = info_task_queue.get()
                law_id = task['law_id']
                law_url = 'https://www.pkulaw.com/chl/'+law_id+'.html?way=homeCommend'
                content = download_info(law_url,cookie_service.get_one_vip_cookie())
                law_info = parse_info(content)
                db_func.save_law_info(law_id, law_info)
                db_func.update_law_crawl_status(law_id,2)
            elif list_task_queue.qsize()>0:
                task = list_task_queue.get()
                cookie = cookie_service.get_one_m_cookie()
                content = download_law_list(task = task, cookie=cookie)
                if parse_m_list(task,content,cookie):
                    db_func.update_list_task(task['id'],2)
            if task is None:
                time.sleep(1)
                continue
            time.sleep(1)
        except Exception as e:
            print(e)

#抓取详情采集流程逻辑
def spider_info():
    while 1:
        try:
            if info_task_queue.qsize() > 100:
                time.sleep(2)
                continue
            laws = db_func.get_need_crawl_laws()
            for law in laws:
                print(law)
                info_task_queue.put(law)
                db_func.update_law_crawl_status(law['law_id'],1)
            time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    params = '{"sorts":[{"sort":"IssueDate","sortOrder":"desc"}],"synonym":false,"analyzer":false,"library":"1469238638146621440","size":10,"page":1,"group":null,"scopes":[{"analyzer":false,"keyword":"XA0101","scopes":["EffectivenessDic"],"synonym":false,"termType":4},{"analyzer":false,"keyword":"1949","scopes":["IssueDate"],"synonym":false,"termType":5},{"analyzer":false,"keyword":"02","scopes":["TimelinessDic"],"synonym":false,"termType":4}],"moreScopes":[],"searchType":3}'
    print(len(json.dumps(json.loads(params))))
    print(len(params))