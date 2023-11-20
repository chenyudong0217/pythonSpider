# encoding: utf-8
import sys
import time
import threading
import loginManage
import Spider
import cookie


if __name__ == '__main__':
    #启动cookie登录线程
    login_manager = threading.Thread(target=loginManage.start)
    login_manager.start()

    cookies = cookie.cookie_service
    ##装载可用cookie
    cookie_manager = threading.Thread(target=cookies.load_cookies)
    cookie_manager.start()

    #启动列表页翻页获取law_id线程
    threading.Thread(target=Spider.spider_law_id)

    #启动详情页抓取线程
    threading.Thread(target=Spider.spider_info)