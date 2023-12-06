# encoding: utf-8
#所有涉及sql操作的函数均整理到该py文件
import sys, os
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.sqlpool import PymysqlPool



def find_account(user_id):
    sql = 'select * from account_table where id='+str(user_id)
    try:
        mysql = PymysqlPool()
        need_login_accounts = mysql.getOne(sql=sql)
        mysql.dispose()
        return need_login_accounts
    except Exception as e:
        print(e)

#查找需要登录的账号信息
def find_need_login_account():
    #需要登录的账号状态，初始is_login=null, cookie时效 is_login=2, cookie超时 currtime-last_login_time > 1 小时
    sql = "select * from account_table where is_login is null or is_login=2 or last_login_time < '"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-1800))+"';"
    try:
        mysql = PymysqlPool()
        need_login_accounts = mysql.getAll(sql=sql)
        mysql.dispose()
        return need_login_accounts
    except Exception as e:
        print(e)

#更新账号表中账号登录状态
def update_account_info(user_id):
    sql = "update account_table set is_login=1, last_login_time=now() where id="+str(user_id)+";"
    try:
        mysql = PymysqlPool()
        mysql.update(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

#保存cookie信息
def add_account_cookie(user_id,www_cookie, m_cookie, cas_cookie,cookie_type):
    sql = "insert into cookie_table (cookie_type, www_cookie, m_cookie, cas_cookie, login_time, user_id) values ("+str(cookie_type)+",'"+www_cookie+"', '"+m_cookie+"', '"+cas_cookie+"', now(),"+str(user_id)+");"
    try:
        mysql = PymysqlPool()
        mysql.insert(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

#根据user_id 删除过期cookie
def del_account_cookie(user_id):
    sql = "delete from cookie_table where user_id = "+str(user_id)+";"
    try:
        mysql = PymysqlPool()
        mysql.delete(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

##查找所有cookie
def find_all_cookie():
    find_all_cookie_sql = 'select * from cookie_table'
    try:
        mysql = PymysqlPool()
        cookies = mysql.getAll(sql=find_all_cookie_sql)
        mysql.dispose()
        return cookies
    except Exception as e:
        print(e)


#获取一条需要采集的法条id
def get_one_need_crawl_law():
    try:
        sql = 'select * from law_id_table where is_crawled = 0 '
        mysql = PymysqlPool()
        law = mysql.getOne(sql=sql)
        mysql.dispose()
        return law
    except Exception as e:
        print(e)

#批量获取需要采集的法条id
#每个批次调出20条
def get_need_crawl_laws():
    try:
        sql = 'select * from law_id_table where is_crawled = 0'
        mysql = PymysqlPool()
        laws = mysql.getMany(sql=sql,num=20)
        mysql.dispose()
        return laws
    except Exception as e:
        print(e)
#更新当前法条采集状态
#0:未采集， 1:采集中，2 采集完成
def update_law_crawl_status(law_id,status):
    try:
        sql = "update law_id_table set is_crawled="+str(status)+" where law_id='"+law_id+"';"
        mysql = PymysqlPool()
        mysql.update(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

def add_law_id(law_id, law_title,law_topic_id, law_column_id):
    try:
        print('add law_id: %s, title: %s',(law_id,law_title))
        sql = "insert into law_id_table (topic_id, column_id,law_id, title, is_crawled) values('"+law_topic_id+"','"+law_column_id+"','"+law_id+"', '"+law_title+"', 0);"
        mysql = PymysqlPool()
        mysql.insert(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

#新增法条标签卡片信息
def save_law_card(law_id, card):
    try:
        sql = "insert into law_info_table(law_id,card) values('"+law_id+"','"+card+"')"
        mysql = PymysqlPool()
        mysql.insert(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

def save_law_info_m(law_id, title, content):
    try:
        sql = "update law_info_table set title='"+title+"', content='"+content+"' where law_id='"+law_id+"'"
        mysql = PymysqlPool()
        mysql.update(sql=sql)
        mysql.dispose()
        print('save law info, law_id:'+law_id)
    except Exception as e:
        print(e)
#新增法条详情
def save_law_info(law_id,law_info):
    try:
        title = law_info['title']
        issue_department = law_info['issueDepartment']
        issue_date = law_info['issueDate']
        implement_date = law_info['implementDate']
        timeliness_dic = law_info['timelinessDic']
        effectiveness_dic = law_info['effectivenessDic']
        category = law_info['category']
        content = law_info['content']
        sql = "insert into law_info_table (law_id,title,issue_department,issue_date,implement_date,timeliness_dic,effectiveness_dic,category,content) values ('"+law_id+"','"+title+"','"+issue_department+"','"+issue_date+"','"+implement_date+"','"+timeliness_dic+"','"+effectiveness_dic+"','"+category+"','"+content+"');"
        mysql = PymysqlPool()
        mysql.insert(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)

#从库中调出需要翻页的列表检索条件

def find_list_params():
    '''执行查找前num条需要抓取的list任务'''
    try:
        sql = 'select id, params from law_list_params_table where is_crawl=0 limit 1'
        mysql = PymysqlPool()
        list_task = mysql.getOne(sql=sql)
        mysql.dispose()
        return list_task
    except Exception as e:
        print(e)

def update_list_task(id,status):
    try:
        sql = 'update law_list_params_table set is_crawl='+str(status)+' where id='+str(id)
        mysql = PymysqlPool()
        mysql.update(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)
def insert_list_params(params):
    try:
        sql = "insert into law_list_params_table (params,is_crawl) values ('"+params+"',0)"
        mysql = PymysqlPool()
        mysql.insert(sql=sql)
        mysql.dispose()
    except Exception as e:
        print(e)