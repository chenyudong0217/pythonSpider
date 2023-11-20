# encoding : utf-8
import sys, os
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.mysqlUtil import mysql_util

mysqlUtil = mysql_util('localhost',3306,'root','root','pkulaw')

find_all_cookie_sql = 'select cookie_type, m_cookie, www_cookie, cas_cookie from cookie_table'

m_cookie_queue = []
vip_www_cookie_queue = []

#释放无效cookie， 删除cookie表对应记录，更新account is_login = 0
def release_cookie(self):
    print('release cookie')
def get_one_vip_cookie():
    try:
        queue_len = len(vip_www_cookie_queue)
        return vip_www_cookie_queue[random.randint(0,queue_len-1)]
        print('随机返回可用vip cookie')
    except Exception as e:
        print(e)

def get_one_m_cookie():
    try:
        queue_len = len(m_cookie_queue)
        return m_cookie_queue[random.randint(0,queue_len-1)]
        print('随机返回一个可用m端cookie')
    except Exception as e:
        print(e)

#周期加载库中可用cookie到字典中，
def load_cookies():
    print('加载db中的可用cookie到 缓存中')
    try:
        while 1:
            m_cookie_queue.clear()
            vip_www_cookie_queue.clear()

            cookies = mysqlUtil.select_data(find_all_cookie_sql)
            for cookie in cookies:
                cookie_type = cookie[0]
                if cookie_type == 1:
                    vip_www_cookie_queue.append(cookie[2])
                else:
                    m_cookie_queue.append(cookie[1]+';'+cookie[3])
            time.sleep(30)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(random.randint(0,10))