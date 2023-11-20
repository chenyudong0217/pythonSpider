# encoding:utf-8
import time
import requests
from bs4 import BeautifulSoup
import queue

import cookie as cookie_service
import law as law_service
info_task_queue = queue.Queue()
list_task_queue = queue.Queue()

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


#下载www站 法条详情页html
def download_info(url ,cookie):
    payload = {}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'www.pkulaw.com',
        'Referer': 'https://www.pkulaw.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    try:
        response = requests.request('GET', url, headers=headers, data=payload)
        return response.text
    except Exception as e:
        print(e)




def spider_law_id():
    print('spider law_list for law id')

def downloader():
    while 1:
        try:
            task = None
            if info_task_queue.qsize()>0:
                task = info_task_queue.get()
            elif list_task_queue.qsize()>0:
                task = list_task_queue.get()
            if task is None:
                time.sleep(1)
                continue
        except Exception as e:
            print(e)

#抓取详情采集流程逻辑
def spider_info():
    while 1:
        try:
            laws = law_service.get_need_crawl_laws()
            for law in laws:
                print(law)
                info_task_queue.put(law)
                law_service.update_law_crawl_status(law[0],1)
        except Exception as e:
            print(e)

if __name__ == '__main__':

    spider_info()