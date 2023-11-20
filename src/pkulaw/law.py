# encoding: utf-8
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from util.mysqlUtil import mysql_util

mysqlUtil = mysql_util('localhost',3306,'root','root','pkulaw')
#获取一条需要采集的法条id
def get_one_need_crawl_law():
    try:
        sql = 'select * from law_id_table where is_crawled = 0 limit 1'
        return mysqlUtil.select_data(sql)
    except Exception as e:
        print(e)

#批量获取需要采集的法条id
#每个批次调出20条
def get_need_crawl_laws():
    try:
        sql = 'select * from law_id_table where is_crawled = 0 limit 20'
        return mysqlUtil.select_data(sql)
    except Exception as e:
        print(e)
#更新当前法条采集状态
#0:未采集， 1:采集中，2 采集完成
def update_law_crawl_status(law_id,status):
    try:
        sql = "update law_id_table set is_crawled="+str(status)+"where law_id='"+law_id+"';"
        mysqlUtil.update_data(sql)
    except Exception as e:
        print(e)


