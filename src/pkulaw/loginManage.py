# encoding: utf-8
import sys, os
import time, datetime
import ChromeCookieServer as chromeServer

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.mysqlUtil import mysql_util

mysqlUtil = mysql_util('localhost',3306,'root','root','pkulaw')



#查找需要登录的账号信息
def find_need_login_account():
    #需要登录的账号状态，初始is_login=null, cookie时效 is_login=2, cookie超时 currtime-last_login_time > 3 小时
    sql = "select * from account_table where is_login is null or is_login=2 or last_login_time < '"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-10800))+"';"
    try:
        need_login_accounts = mysqlUtil.select_data(sql)
        return need_login_accounts
    except Exception as e:
        print(e)

#更新账号表中账号登录状态
def update_account_info(user_id):
    sql = "update account_table set is_login=1, last_login_time=now() where id="+str(user_id)+";"
    try:
        mysqlUtil.update_data(sql)
    except Exception as e:
        print(e)

def add_account_cookie(user_id,www_cookie, m_cookie, cas_cookie,cookie_type):
    sql = "insert into cookie_table (cookie_type, www_cookie, m_cookie, cas_cookie, login_time, user_id) values ("+str(cookie_type)+",'"+www_cookie+"', '"+m_cookie+"', '"+cas_cookie+"', now(),"+str(user_id)+");"
    try:
        mysqlUtil.insert_data(sql)
    except Exception as e:
        print(e)

#获取需要登录账号信息，实现模拟登录，更新cookie表
def login():
    need_login_accounts = find_need_login_account()
    for account in need_login_accounts:
        try:
            user_id = account[0]
            phone = account[3]
            password = account[2]
            user_type = account[5]
            cookie_dict = chromeServer.do_login(phone, password)
            add_account_cookie(user_id,cookie_dict['www_cookie'], cookie_dict['m_cookie'],cookie_dict['cas_cookie'],user_type)
            update_account_info(user_id)
            time.sleep(10)
        except Exception as e:
            print(e)

#启动账号登录流程
def start():
    while 1:
        login()
        time.sleep(30)

if __name__ == '__main__':

    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-21600)))
