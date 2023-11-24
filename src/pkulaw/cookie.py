# encoding : utf-8
import random
import time
import db_func
import loginManage
m_cookie_queue = []
vip_www_cookie_queue = []

#释放无效cookie， 删除cookie表对应记录，更新account is_login = 0
def release_cookie(cookie):
    print('release cookie')
    user_id = cookie['user_id']
    account = db_func.find_account(user_id)
    cookie_type = cookie['cookie_type']
    db_func.del_account_cookie(user_id)
    loginManage.login_account(user_id,account['phone'],account['password'],cookie_type)
    db_func.update_account_info(user_id)


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
    while 1:
        try:
            m_cookie_queue.clear()
            vip_www_cookie_queue.clear()
            cookies = db_func.find_all_cookie()
            for cookie in cookies:
                cookie_type = cookie['cookie_type']
                if cookie_type == 1:
                    vip_www_cookie_queue.append(cookie)
                else:
                    m_cookie_queue.append(cookie)
            time.sleep(30)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    load_cookies()