# encoding: utf-8
import  requests
from bs4 import BeautifulSoup
import CryptoJsUtil as cryptojs
import json,time
import urllib.parse
from Spider import proxy_queue
encryptionKey = '25597edaee9e4eddb07f2d4d1a09eb49'

#基于临时会话code 请求token信息
def get_token(code):
    token = ''
    url = "https://cas.pkulaw.com/auth/realms/fabao/protocol/openid-connect/token"
    payload = 'code='+code+'&grant_type=authorization_code&client_id=WEB&redirect_uri=https%3A%2F%2Fm.pkulaw.com%2F'
    header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Content-Length': '202',
              'Content-type': 'application/x-www-form-urlencoded',
              'Host': 'cas.pkulaw.com',
              'Origin': 'https://m.pkulaw.com',
              'Referer': 'https://m.pkulaw.com/',
              'Sec-Fetch-Site': 'same-site',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
              }
    try:
        # proxyIp = proxy_queue.get()
        # outDateTs = proxyIp['outDateTs']
        # while int(time.time()) > outDateTs:
        #     proxyIp = proxy_queue.get()
        #     outDateTs = proxyIp['outDateTs']
        # proxy = {'http':str(proxyIp['address']),'https':str(proxyIp['address'])}
        response = requests.request("POST", url, headers=header, data=payload)
        token = json.loads(response.text)['access_token']
    except Exception as e:
        print(e)
    return token


def get_login_code(url, username, password, encryptionKey, cookie):
    code = ''
    payload = {'loginType': 1,
               'redirect_uri': 'https://m.pkulaw.com/',
               'email-phone': username,
               'password': password,
               'encryptionKey': encryptionKey}
    headers = {
        'Host': 'cas.pkulaw.com',
        'Content-Length':str(len(urllib.parse.urlencode(payload))),
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie
    }
    # proxyIp = proxy_queue.get()
    # outDateTs = proxyIp['outDateTs']
    # while int(time.time()) > outDateTs:
    #     proxyIp = proxy_queue.get()
    #     outDateTs = proxyIp['outDateTs']
    # proxy = {'http':str(proxyIp['address']),'https':str(proxyIp['address'])}

    response = requests.request("POST", url, headers=headers, data=payload,allow_redirects=False)
    set_cookie = response.headers.get('set-cookie')
    location = response.headers.get('location')
    if location.__contains__('&code='):
        code = location.split('&code=')[1]
    if location.__contains__('?code='):
        code = location.split('?code=')[1]
    return code

#打开登录页，获取登录会话参数
def open_login_html():
    url = "https://cas.pkulaw.com/auth/realms/fabao/protocol/openid-connect/auth?scope=openid&response_type=code&client_id=pkulaw&redirect_uri=https://m.pkulaw.com/"
    payload = {}
    headers = {}
    # proxyIp = proxy_queue.get()
    # outDateTs = proxyIp['outDateTs']
    # while int(time.time()) > outDateTs:
    #     proxyIp = proxy_queue.get()
    #     outDateTs = proxyIp['outDateTs']
    # proxy = {'http':str(proxyIp['address']),'https':str(proxyIp['address'])}
    response = requests.request("GET", url, headers=headers, data=payload)
    content = response.text
    login_param = {}
    set_cookies = response.cookies
    cookie_str = ''
    for cookie in set_cookies:
        cookie_str = cookie_str+cookie.name+'='+cookie.value+';'
    login_param['login_cookie'] = str(cookie_str)

    soup = BeautifulSoup(content, 'html.parser')
    login_form_node = soup.find('form',attrs={'id':'kc-form-login'})
    login_url = login_form_node.get('action')
    login_param['login_url'] = str(login_url)

    encryptionKey_node = soup.find('input',attrs={'id':'encryptionKey'})
    encryptionKey = encryptionKey_node.get('value')
    login_param['encryptionKey'] = str(encryptionKey)
    return login_param


##m站账号登录，获取可用authorization
def login(username, password):
    login_param = open_login_html();
    code = get_login_code(login_param['login_url'], username, cryptojs.encryption(password, login_param['encryptionKey']),login_param['encryptionKey'],login_param['login_cookie'])
    token = get_token(code)
    return token
if __name__ == '__main__':
    print(login('15837466531','DA2023da'))

