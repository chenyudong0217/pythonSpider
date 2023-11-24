# encoding: utf-8
import json
from src.util.mysqlUtil import mysql_util
mysqlUtil = mysql_util('localhost',3306,'root','root','pkulaw')

if __name__ == '__main__':

    with open('flfg.txt','r',encoding='utf-16') as file:
        for line in file:
            try:
                result = json.loads(line)
                if result['code'] == 200:
                    laws = result['data']['info']
                    for law in laws:
                        print(law)
                        insert_law_sql = "insert into law_id_table (topic_id, column_id,law_id, title, is_crawled) values ('"+law['topicId']+"', '"+law['columnId']+"', '"+law['gid']+"', '"+law['title']+"', 0);"
                        mysqlUtil.insert_data(insert_law_sql)

            except Exception as e:
                print(e)

