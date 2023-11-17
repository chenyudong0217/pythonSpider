# encoding:utf-8
import time
import requests
from bs4 import BeautifulSoup

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


def test(url, cookie):
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
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    print(parse_info(response.text))


if __name__ == '__main__':
    cookie = 'xCloseNew=17;Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1700117707;authormes=efed66a30653717245e4db4596782e296fea1d25d173b373b73dc5c71c7f22c5973cbbc7b114eedabdfb;double11_2023=true;userislogincookie=true;__tst_status=3355752069#;Hm_up_8266968662c086f34b2a3e2ae9014bf8=%7B%22ysx_yhqx_20220602%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22ysx_hy_20220527%22%3A%7B%22value%22%3A%2201%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22cf0b5347-e282-ee11-b943-d46cc8e17ef0%22%2C%22scope%22%3A1%7D%2C%22ysx_yhjs_20220602%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%7D;SUB_LEGACY=37d155a1-ee73-4fea-8804-8afc959229b5;pkulaw_v6_sessionid=bg4kbylsz0mqobxu5rgtlc1w;SUB=37d155a1-ee73-4fea-8804-8afc959229b5;KC_ROOT_LOGIN_LEGACY=1;Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1700117686;KC_ROOT_LOGIN=1;CookieId=20928bf34ddb978c75a155d8240614e4;referer=;LoginAccount=phone2023111419380736864;referer=https://www.pkulaw.com/;CookieId_LEGACY=20928bf34ddb978c75a155d8240614e4;'
    for i in range(0,50):
        test('https://www.pkulaw.com/chl/8d665e8d2c7a832fbdfb.html?way=homeCommend',cookie)
        time.sleep(0.5)
    print('start pkulaw spider')