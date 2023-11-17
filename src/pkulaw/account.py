# encoding: utf-8
import  requests
from bs4 import BeautifulSoup
import CryptoJsUtil as cryptojs
import json

encryptionKey = '25597edaee9e4eddb07f2d4d1a09eb49'


##基于登录cookie 获取临时code
def get_code(login_cookie):
    code = ''
    url = 'https://cas.pkulaw.com/auth/realms/fabao/protocol/openid-connect/auth?client_id=WEB&redirect_uri=https%3A%2F%2Fm.pkulaw.com%2F&response_mode=fragment&response_type=code&scope=openid&prompt=none'
    payload = {}
    headers = {'Host': 'cas.pkulaw.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Referer': 'https://m.pkulaw.com/',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cookie':login_cookie}
    try:

        response = requests.request("GET", url, headers=headers, data= payload, allow_redirects=False) ##禁止自动重定向
        location = response.headers.get('location')
        if location.__contains__('&code='):
            code = location.split('&code=')[1]
    except Exception as e:
        print(e)
    return code

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
              'Content-type': ' application/x-www-form-urlencoded',
              'Host': ' cas.pkulaw.com',
              'Origin': ' https://m.pkulaw.com',
              'Referer': ' https://m.pkulaw.com/',
              'Sec-Fetch-Site': ' same-site',
              'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
              }
    try:
        response = requests.request("POST", url, headers=header, data=payload)
        token = json.loads(response.text)['access_token']
    except Exception as e:
        print(e)
    return token




def login_request(username, password, encryptionKey):
    url = 'https://cas.pkulaw.com/auth/realms/fabao/sms/check-username-login?username='+username+'&password='+password+'&encryptionKey='+encryptionKey
    payload = {}
    headers = {
        'Host': 'cas.pkulaw.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    print(response.headers)

def login_request_post(url, username, password, encryptionKey, cookie):
    payload = {'loginType': '1',
               'redirect_uri': 'https://www.pkulaw.com/',
               'email-phone': username,
               'password': password,
               'encryptionKey': encryptionKey}
    headers = {
        'Host': 'cas.pkulaw.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response.text
    set_cookies = response.headers.get('set-cookie')
    set_cookies = response.cookies
    cookie_str = ''
    logined_param = {}
    for cookie in set_cookies:
        cookie_str = cookie_str+cookie.name+'='+cookie.value+';'
    logined_param['logined_cookie'] = str(cookie_str)
    return logined_param
def open_login_html():
    url = "https://cas.pkulaw.com/auth/realms/fabao/protocol/openid-connect/auth?scope=openid&response_type=code&client_id=pkulaw&redirect_uri=https://www.pkulaw.com/"
    payload = {}
    headers = {}
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
def login(username, password):
    login_param = open_login_html();

    logined_param = login_request_post(login_param['login_url'], username, cryptojs.encryption(password, login_param['encryptionKey']),login_param['encryptionKey'],login_param['login_cookie'])

    print(str(logined_param['logined_cookie']))




if __name__ == '__main__':

    login('18851677310','qq123456789')
