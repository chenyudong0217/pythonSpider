# encoding: utf-8
import sys
import time
import threading
import loginManage
import Spider
import cookie


if __name__ == '__main__':
    #启动cookie登录线程
    #login_manager = threading.Thread(target=loginManage.start)
    #login_manager.start()

    #cookies = cookie.cookie_service
    ##装载可用cookie
    cookie_manager = threading.Thread(target=cookie.load_cookies)
    cookie_manager.start()

    download_work = threading.Thread(target=Spider.downloader)
    download_work.start()
    #启动列表页翻页获取law_id线程
    list_schedule = threading.Thread(target=Spider.spider_law_id)
    list_schedule.start()
    #启动详情页抓取线程
    info_schedule = threading.Thread(target=Spider.spider_info)
    #info_schedule.start()