# encoding: utf-8
import sys, os
import time, datetime
import ChromeCookieServer as chromeServer
import db_func


#获取需要登录账号信息，实现模拟登录，更新cookie表
def login():
    need_login_accounts = db_func.find_need_login_account()
    for account in need_login_accounts:
        try:
            user_id = account['id']
            phone = account['phone']
            password = account['password']
            user_type = account['user_type']
            cookie_dict = chromeServer.do_login(phone, password)
            db_func.del_account_cookie(user_id)
            db_func.add_account_cookie(user_id,cookie_dict['www_cookie'], cookie_dict['m_cookie'],cookie_dict['cas_cookie'],user_type)
            db_func.update_account_info(user_id)
            time.sleep(10)
        except Exception as e:
            print(e)

#启动账号登录流程
def start():
    while 1:
        try:
            login()
            time.sleep(30)
        except Exception as e:
            print(e)
if __name__ == '__main__':
    start()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-21600)))
