#encoding:utf-8
from selenium import webdriver

from selenium.webdriver.common.by import By
import time

def init_webdriver():

    chrome_options = webdriver.ChromeOptions()
    ##chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-javascript')
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    ##chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
    chrome_service = webdriver.ChromeService(executable_path=r'D:\chromedriver\chrome104\chromedriver.exe');
    driver = webdriver.Chrome(options=chrome_options,service=chrome_service)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    driver.get("https://m.pkulaw.com/pages/usercenter/index")
    driver.get_cookies()
    time.sleep(5)
    return driver


def do_login(user, password, driver):
    try:
        login_node = driver.find_element(By.XPATH, '//uni-view[@class="tBtn"]')
        login_node.click()
        time.sleep(5)
        ## 登陆页输入用户名密码登陆
        input_email_node = driver.find_element(By.XPATH,'//input[@id="email-phone"]')
        input_email_node.clear()
        input_email_node.send_keys(user)

        input_password_node = driver.find_element(By.XPATH,'//input[@id="passwordFront"]')
        input_password_node.clear()
        input_password_node.send_keys(password)

        login_node = driver.find_element(By.XPATH, '//div[@class="form-btn"]/a[@class="blue"]')
        login_node.click()
        time.sleep(10)
        dynamic_cookie = driver.execute_script("return document.cookie;")
        print(dynamic_cookie)
        account_cookie = ''
        cookies = driver.get_cookies()
        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            account_cookie = account_cookie+cookie_name+'='+cookie_value+';'
        print(account_cookie)
        account_cookie = ''
        driver.get('https://www.pkulaw.com/')
        time.sleep(5)
        driver.get('https://www.pkulaw.com/chl/8d665e8d2c7a832fbdfb.html?way=homeCommend')
        time.sleep(5)
        cookies = driver.get_cookies()
        for cookie in cookies:
            cookie_name = cookie['name']
            cookie_value = cookie['value']
            account_cookie = account_cookie+cookie_name+'='+cookie_value+';'

        print(account_cookie)
        return account_cookie
    except Exception as e:
        print(e)

if __name__ == '__main__':

    try:
        driver = init_webdriver()
        do_login('18851677310','qq123456789',driver)
    except Exception as e:
        print(e)
